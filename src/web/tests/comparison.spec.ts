import { expect, test, type Page } from '@playwright/test';
const evidence=process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-11-slice-05-release';

// Controlled HTTP responses only. This file makes no provider, Bedrock, or AWS call.
async function setup(page:Page, options:{empty?:boolean; uncertain?:boolean; unresolved?:boolean}={}) {
  await page.goto('/');await page.getByRole('button',{name:'Continue with local identity'}).click();
  await page.getByLabel('Fictional bank name').fill(`Fictional comparison bank ${Date.now()}`);
  await page.getByLabel('I confirm this case contains fictional data only.',{exact:true}).check();
  await page.getByRole('button',{name:'Save fictional case',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Documents',exact:true})).toBeVisible();
  const config=await (await page.request.get('/config.json')).json();
  const caseId=new URL(page.url()).searchParams.get('case')!,root=`${config.api_url}/api/cases/${caseId}`;
  const source=(id:string,version:string,text:string)=>({document:{case_id:caseId,source_id:'RBI-TEST',version,
    document_version_id:id,kind:'regulation',synthetic:false,source_url:'https://www.rbi.org.in/',
    publication_date:version==='older'?'2023-01-01':'2024-01-01',effective_date:version==='older'?'2023-04-01':'2024-04-01'},
    filename:'Controlled test source',authority:'Reserve Bank of India',freshness:'unverified',
    passages:[{document_version_id:id,passage_id:`${id}-clause`,location:'Test clause',text}]});
  const older=source('reg-old-test','older','Controlled test: Review access.'),newer=source('reg-new-test','newer','Controlled test: Require independent approval.');
  const citation=(s:any)=>({...s.passages[0],quote:s.passages[0].text,text:undefined});
  const obligation=(s:any)=>({obligation_id:'RULE-1',requirement:s.passages[0].text,conditions:['Selected condition'],
    exceptions:['Selected exception'],applicability:'Selected fictional bank',citations:[citation(s)]});
  const finding=(id:string)=>({finding_id:id,obligation_id:'RULE-1',control_ids:['ACCESS-01'],status:'needs_review',
    rationale:'Controlled interpretation needs review.',primary_recommendation:'Inspect fictional records.',citations:[citation(older)],
    evidence_condition:'missing',gap_kind:'evidence'});
  const result=(job:string,newRun=false)=>({job:{job_id:job,state:'completed',model_calls:1,stop_reason:null,unchecked_obligations:[]},
    snapshot:{snapshot_id:newRun?'new-snapshot':'comparison-baseline',case_id:caseId,assessment_date:'2024-05-01',
      selected_versions:{'RBI-TEST':newRun?'newer':'older',bank:'1'},selected_obligations:['RULE-1'],model_version:'pinned-model',prompt_version:'assessment-vs5-selected-period-v1'},
    data_mode:'synthetic_live',freshness:'unverified',live_model_calls:1,findings:[finding(newRun?'new-finding':'old-finding')],
    reviews:newRun?[]:[{event_id:'old-review',finding_id:'old-finding',event_kind:'final_review',disposition:'approved',revision:1,
      committed_at:'2026-10-11T10:00:00Z',accepted_content:{status:'needs_review',rationale:'Earlier original review',recommendation:'Inspect records'}}],
    obligations:[obligation(newRun?newer:older)],controls:[],obligation:null,control:null,
    summary:{cutoff:'2026-10-11T10:00:00Z',eligible:1,reviewed:newRun?0:1,approved:newRun?0:1,edited:0,rejected:0,
      pending:newRun?1:0,approval_rate:newRun?null:1,edit_rate:0,rejection_rate:0,adoption_rate:newRun?null:1,review_coverage:newRun?0:1},trace:{attempts:[]}});
  let exists=false,complete=false,newJob:string|null=null,uncertain=!!options.uncertain;
  const keys:string[]=[],reviewBodies:any[]=[];
  const comparison=()=>({comparison_id:'saved-native-comparison',case_id:caseId,snapshot_id:'comparison-baseline',job_id:'comparison-job',
    baseline_job_id:'comparison-baseline-job',new_job_id:newJob,data_mode:'synthetic_live',freshness:'unverified',
    assessment_context:{assessment_date:'2024-05-01',selected_versions:{'RBI-TEST':'older',bank:'1'},selected_obligations:['RULE-1']},
    state:complete?'completed':'queued',model_calls:complete?1:0,stop_reason:null,unchecked_obligations:complete?[]:['RULE-1'],
    older_source:older,newer_source:newer,trace:[],result:complete?{snapshot_id:'comparison-baseline',older_version_id:'reg-old-test',newer_version_id:'reg-new-test',
      changes:[{obligation_id:'RULE-1',kind:options.unresolved?'undetermined':'changed_requirement',before:obligation(older),after:obligation(newer),
        reason:'Controlled cited interpretation.',basis:[citation(older),citation(newer)],affected_control_ids:options.unresolved?[]:['ACCESS-01']}],
      affected_control_ids:options.unresolved?[]:['ACCESS-01'],unresolved_obligation_ids:options.unresolved?['RULE-1']:[],
      assessment_required:!options.unresolved,selection_review_required:true,metadata_changes:{effective_date:{older:'2023-04-01',newer:'2024-04-01'}}}:null});
  await page.route(`${root}/assessments**`,route=>{
    const path=new URL(route.request().url()).pathname.slice(new URL(root).pathname.length);
    if(path==='/assessments')return route.fulfill({json:{runs:[{job_id:'comparison-baseline-job',job_admitted_at:'2026-10-11T10:00:00Z'}]}});
    if(path==='/assessments/comparison-baseline-job')return route.fulfill({json:result('comparison-baseline-job')});
    if(path==='/assessments/new-comparison-assessment')return route.fulfill({json:result('new-comparison-assessment',true)});
    return route.fulfill({status:404,json:{message:'Unavailable controlled route'}});
  });
  await page.route(`${root}/regulatory-comparisons**`,route=>{
    const url=new URL(route.request().url()),path=url.pathname.slice(new URL(root).pathname.length),method=route.request().method();
    if(path==='/regulatory-comparisons/selection')return route.fulfill({json:{case_id:caseId,snapshot_id:url.searchParams.get('snapshot_id'),
      baseline_job_id:url.searchParams.get('snapshot_id')==='comparison-baseline'?'comparison-baseline-job':'new-comparison-assessment',
      assessment_date:'2024-05-01',selected_versions:{'RBI-TEST':'older',bank:'1'},selected_obligations:['RULE-1'],
      freshness:'unverified',older_versions:[older],newer_versions:options.empty?[]:[newer]}});
    if(path==='/regulatory-comparisons'&&method==='GET')return route.fulfill({json:{comparisons:exists?[{...comparison(),result:undefined}]:[]}});
    if(path==='/regulatory-comparisons'&&method==='POST') {
      const body=route.request().postDataJSON();keys.push(body.idempotency_key);exists=true;
      expect(body).toMatchObject({older_version_id:'reg-old-test',newer_version_id:'reg-new-test',snapshot_id:'comparison-baseline'});
      if(uncertain){uncertain=false;return route.fulfill({status:503,json:{message:'Delivery could not be confirmed.',next_action:'Refresh the saved comparison.'}});}
      return route.fulfill({status:202,json:comparison()});
    }
    if(path==='/regulatory-comparisons/saved-native-comparison')return route.fulfill({json:comparison()});
    if(path.endsWith('/reassess')) {
      reviewBodies.push(route.request().postDataJSON());newJob='new-comparison-assessment';
      return route.fulfill({status:202,json:{job_id:newJob,snapshot_id:'new-snapshot'}});
    }
    return route.fulfill({status:404,json:{message:'Unavailable controlled route'}});
  });
  await page.getByRole('button',{name:'Refresh assessment',exact:true}).click();
  await page.getByLabel('Saved assessments',{exact:true}).selectOption('comparison-baseline-job');
  await expect(page.getByRole('region',{name:'Assessment result',exact:true})).toContainText('Approved · Revision 1');
  await page.getByRole('button',{name:'Compare regulatory versions',exact:true}).click();
  const panel=page.getByRole('region',{name:'Saved regulatory comparison',exact:true});
  await expect(panel.getByLabel('Older saved version',{exact:true})).toBeVisible();
  return {panel,keys,reviewBodies,root,value:comparison,complete:()=>{complete=true;},choose:async()=>{
    await panel.getByLabel('Newer saved version',{exact:true}).selectOption('reg-new-test');
    await panel.getByRole('button',{name:'Compare saved versions',exact:true}).click();
  }};
}

test('VS5-CF10 saved comparison shows progress, citations, reload, and independent reviews',async({page})=>{
  const s=await setup(page);await s.choose();await expect(s.panel).toContainText('Comparison queued');
  s.complete();await s.panel.getByRole('button',{name:'Refresh comparison',exact:true}).click();
  await expect(s.panel).toContainText('Changed requirement');await expect(s.panel).toContainText('ACCESS-01');
  await expect(s.panel).toContainText('Selected condition');await expect(s.panel).toContainText('Selected exception');
  await expect(s.panel).toContainText('Controlled test: Require independent approval.');
  await expect(s.panel).toContainText('Current status unverified');
  const start=s.panel.getByRole('button',{name:'Start new assessment',exact:true});await expect(start).toBeDisabled();
  await s.panel.getByLabel('I reviewed the newer version and unchanged assessment inputs.',{exact:true}).check();
  await start.click();expect(s.reviewBodies).toEqual([{selection_reviewed:true}]);
  const result=page.getByRole('region',{name:'Assessment result',exact:true});
  await expect.poll(()=>new URL(page.url()).searchParams.get('assessment')).toBe('new-comparison-assessment');
  await expect(result).toContainText('Pending: 1');await expect(result).not.toContainText('Approved · Revision 1');
  await s.panel.getByRole('button',{name:'Open previous assessment',exact:true}).click();await expect(result).toContainText('Approved · Revision 1');
  await page.reload();await page.getByRole('button',{name:'Continue with local identity',exact:true}).click();
  await page.getByRole('button',{name:'Compare regulatory versions',exact:true}).click();
  await page.getByLabel('Saved regulatory comparisons',{exact:true}).selectOption('saved-native-comparison');
  await expect(page.getByRole('region',{name:'Saved regulatory comparison',exact:true})).toContainText('Changed requirement');
  await page.screenshot({path:`${evidence}/comparison-flow-desktop.png`,fullPage:true});
});

test('VS5-CF11 uncertain comparison keeps its request key through refresh and retry',async({page})=>{
  const s=await setup(page,{uncertain:true});await s.choose();
  await expect(s.panel.getByRole('alert')).toContainText('Delivery could not be confirmed');
  await expect(s.panel.getByRole('button',{name:'Compare saved versions',exact:true})).toBeDisabled();
  await s.panel.getByRole('button',{name:'Refresh comparison',exact:true}).click();await s.choose();
  expect(s.keys).toHaveLength(2);expect(s.keys[1]).toBe(s.keys[0]);
});

test('VS5-CF12 empty saved versions and unresolved changes cannot start reassessment',async({page})=>{
  let s=await setup(page,{empty:true});await expect(s.panel).toContainText('No other saved regulatory version is available');
  await expect(s.panel.getByRole('button',{name:'Compare saved versions',exact:true})).toBeDisabled();
  await page.goto('/');s=await setup(page,{unresolved:true});await s.choose();s.complete();
  await s.panel.getByRole('button',{name:'Refresh comparison',exact:true}).click();await expect(s.panel).toContainText('Undetermined');
  await expect(s.panel.getByRole('button',{name:'Start new assessment',exact:true})).toBeDisabled();
  expect(s.reviewBodies).toEqual([]);
});

test('VS5-CF11 mobile selection and cited results fit the viewport and support keyboard actions',async({page})=>{
  await page.setViewportSize({width:390,height:844});const s=await setup(page);
  const select=s.panel.getByLabel('Newer saved version',{exact:true});await select.selectOption('reg-new-test');await select.focus();
  await page.keyboard.press('Tab');await expect(s.panel.getByRole('button',{name:'Compare saved versions',exact:true})).toBeFocused();
  await page.keyboard.press('Enter');s.complete();await s.panel.getByRole('button',{name:'Refresh comparison',exact:true}).click();
  await expect(s.panel).toContainText('Changed requirement');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
  await s.panel.screenshot({path:`${evidence}/comparison-flow-mobile.png`});
});

test('VS5-CF04 refresh requires the exact saved comparison ID',async({page})=>{
  const s=await setup(page);await s.choose();s.complete();
  await page.route(`${s.root}/regulatory-comparisons/saved-native-comparison`,route=>route.fulfill({
    json:{...s.value(),comparison_id:'different-comparison'}}));
  await s.panel.getByRole('button',{name:'Refresh comparison',exact:true}).click();
  await expect(s.panel.getByRole('alert')).toContainText('could not be confirmed');
  await expect(s.panel).toContainText('Comparison queued');
  expect(new URL(page.url()).searchParams.get('comparison')).toBe('saved-native-comparison');
});
