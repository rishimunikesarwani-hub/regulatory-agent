import { test, expect, type Page } from '@playwright/test';
test.setTimeout(30_000);

// Controlled protocol responses. No AWS service or live model is contacted.
const web = process.env.LOCAL_TEST_WEB_URL || 'http://127.0.0.1:5185';
const api = 'https://api.example.test';
const identity = 'https://demo.auth.ap-south-1.amazoncognito.com';
const storage = 'https://test-documents.s3.ap-south-1.amazonaws.com/report?versionId=pinned';
async function setup(page: Page, enabled = true, destination = storage) {
  const calls: string[] = [];
  const record = {case_id:'cloud-case',owner_id:'operator',bank_profile:{name:'Fictional assessment bank'},synthetic:true,created_at:'2026-10-11T10:00:00Z'};
  const bank = {document:{case_id:'cloud-case',source_id:'policy',version:'1',document_version_id:'policy-1',kind:'policy',synthetic:true},filename:'policy.txt',format:'txt'};
  const regulation = {document:{case_id:'cloud-case',source_id:'RBI',version:'2023',document_version_id:'RBI-2023',kind:'regulation',effective_date:'2023-11-07',source_url:'https://www.rbi.org.in/'},filename:'Historical RBI excerpt'};
  const citation = {document_version_id:'policy-1',passage_id:'policy-1-501',location:'Line 501',quote:'Exact final fictional line.'};
  const result = {job:{job_id:'native-job',state:'completed',model_calls:1,stop_reason:null,unchecked_obligations:[]},
    snapshot:{snapshot_id:'snapshot-one',case_id:'cloud-case',assessment_date:'2024-04-08',selected_versions:{RBI:'2023',policy:'1'},selected_obligations:['RBI-1'],model_version:'pinned-model',prompt_version:'pinned-prompt'},
    data_mode:'synthetic_live',freshness:'unverified',live_model_calls:1,
    findings:[{finding_id:'finding-one',obligation_id:'RBI-1',control_ids:[],status:'needs_review',rationale:'Review the fictional evidence.',primary_recommendation:'Request evidence.',citations:[citation],evidence_condition:'policy_only',gap_kind:null}],
    obligations:[{obligation_id:'RBI-1',requirement:'Inspect selected evidence.',applicability:null,conditions:[],exceptions:[],citations:[]}],controls:[],reviews:[],
    summary:{cutoff:'2026-10-11T10:00:00Z',eligible:1,reviewed:0,approved:0,edited:0,rejected:0,pending:1,approval_rate:null,edit_rate:null,rejection_rate:null,adoption_rate:null,review_coverage:0},trace:{attempts:[]}};
  await page.route('**/config.json',route=>route.fulfill({json:{mode:'aws',api_url:api,cognito_domain:identity,user_pool_client_id:'test-client',redirect_uri:`${web}/`,...(enabled?{assessments_enabled:true}:{})}}));
  await page.route(`${identity}/**`,route=>{
    const url=new URL(route.request().url());
    if(url.pathname==='/oauth2/authorize') {
      const callback=new URL(`${web}/?case=cloud-case`);callback.searchParams.set('code','fictional');callback.searchParams.set('state',url.searchParams.get('state')!);
      return route.fulfill({status:302,headers:{location:callback.href}});
    }
    return route.fulfill({json:{access_token:'fictional-token',token_type:'Bearer',expires_in:900}});
  });
  await page.route(`${api}/api/cases**`,route=>{
    expect(route.request().headers().authorization).toBe('Bearer fictional-token');
    const url=new URL(route.request().url()),path=url.pathname.replace('/api/cases/cloud-case','');calls.push(path);
    if(url.pathname==='/api/cases')return route.fulfill({json:{cases:[record]}});
    if(!path)return route.fulfill({json:record});
    if(path==='/documents')return route.fulfill({json:{sources:[bank]}});
    if(path==='/assessment-selection')return route.fulfill({json:{sources:[bank,regulation],obligations:[{obligation_id:'RBI-1',document_version_id:'RBI-2023',label:'Selected RBI clause'}],data_mode:'synthetic_live',freshness:'unverified',current_available:false}});
    if(path==='/assessments')return route.fulfill({json:{runs:[]}});
    if(path==='/assessments/selected') {
      expect(route.request().postDataJSON()).toMatchObject({selected_versions:{RBI:'2023',policy:'1'},selected_obligations:['RBI-1'],mode:'historical'});
      return route.fulfill({status:202,json:{job_id:'native-job'}});
    }
    if(path==='/assessments/native-job')return route.fulfill({json:result});
    if(path==='/assessments/native-job/sources/policy-1') {
      const offset=Number(url.searchParams.get('offset')||0);
      return route.fulfill({json:{...bank,offset,passage_count:501,next_offset:offset===0?500:null,
        passages:offset===0?[{passage_id:'policy-1-1',location:'Line 1',text:'First fictional line.'}]:[{passage_id:'policy-1-501',location:'Line 501',text:citation.quote}]}});
    }
    if(path==='/assessments/native-job/export')return route.fulfill({json:{url:destination,filename:'assessment-native-job.json'}});
    return route.fulfill({status:404,json:{message:'Unavailable controlled route'}});
  });
  await page.route('https://test-documents.s3.ap-south-1.amazonaws.com/**',route=>{
    expect(route.request().headers().authorization).toBeUndefined();
    return route.fulfill({body:JSON.stringify({sources:['all 501 passages']}),headers:{'Content-Disposition':'attachment; filename="assessment-native-job.json"','Content-Type':'application/json'}});
  });
  await page.goto('/?case=cloud-case');await page.getByRole('button',{name:'Sign in securely'}).click();
  await expect(page.getByRole('heading',{name:'Documents',exact:true})).toBeVisible();
  return calls;
}
async function start(page:Page) {
  await expect(page.getByRole('heading',{name:'Selected historical assessment',exact:true})).toBeVisible({timeout:5000});
  await page.getByLabel('policy.txt · Version 1',{exact:true}).check();
  await page.getByLabel('Selected RBI clause',{exact:true}).check();
  await page.getByLabel('Assessment date',{exact:true}).fill('2024-04-08');
  await page.getByRole('button',{name:'Run selected assessment with live model',exact:true}).click();
  await expect(page.getByRole('region',{name:'Assessment result',exact:true})).toBeVisible();
}
test('VS5-CA15 cloud flag defaults off without assessment traffic',async({page})=>{
  const calls=await setup(page,false);
  await expect(page.getByRole('heading',{name:'Assessment',exact:true})).toHaveCount(0);
  expect(calls.some(path=>path.includes('assessment'))).toBe(false);
});
test('VS5-CA15 selected cloud flow pages sources and downloads private artifacts without bearer token',async({page})=>{
  const calls=await setup(page);await start(page);
  await page.screenshot({path:'../../runs/2026-10-11-slice-05-release/cloud-api-desktop.png',fullPage:true});
  await expect(page.getByRole('button',{name:'Run controlled assessment',exact:true})).toHaveCount(0);
  expect(calls).not.toContain('/comparisons');
  await page.getByRole('button',{name:'Inspect Line 501',exact:true}).click();
  await page.getByRole('button',{name:'Next source passages',exact:true}).click();
  await expect(page.getByRole('dialog')).toContainText('Exact final fictional line.');
  await page.getByRole('dialog').screenshot({path:'../../runs/2026-10-11-slice-05-release/cloud-api-source.png'});
  await page.getByRole('button',{name:'Previous source passages',exact:true}).click();
  await expect(page.getByRole('dialog')).toContainText('First fictional line.');
  await page.getByRole('button',{name:'Close source',exact:true}).click();
  const download=page.waitForEvent('download');await page.getByRole('button',{name:'Download JSON',exact:true}).click();
  expect((await download).suggestedFilename()).toBe('assessment-native-job.json');
});
test('VS5-CA15 rejects a private download with credentials in its URL',async({page})=>{
  await setup(page,true,'https://user:password@test-documents.s3.ap-south-1.amazonaws.com/report');await start(page);
  let downloads=0;page.on('download',()=>downloads++);
  await page.getByRole('button',{name:'Download JSON',exact:true}).click();
  await expect(page.getByRole('alert')).toBeVisible();expect(downloads).toBe(0);
});
