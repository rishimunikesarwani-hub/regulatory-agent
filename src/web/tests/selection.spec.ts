import { expect, test, type Page } from '@playwright/test';
const evidence = process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-11-slice-05-release';

test('VS5-EP11 source inspection shows stated dates and their exact grounding without claiming operation', async ({page}) => {
  const s = await setup(page); await s.choose();
  const uploaded = await page.request.post(`${s.root}/documents`,{data:Buffer.from(
    'FICTIONAL DATA ONLY\n2024-04-01 to 2024-04-07: Access records were reviewed.\n'),headers:{
    'Content-Type':'application/octet-stream','X-Filename':'dated-fiction.txt','X-Document-Kind':'evidence','X-Synthetic':'true'}});
  expect(uploaded.status()).toBe(201);
  const dated = await uploaded.json();
  const record = dated.passages[1];
  const citation = {document_version_id:dated.document.document_version_id,passage_id:record.passage_id,
    location:record.location,quote:'2024-04-01 to 2024-04-07'};
  dated.stated_periods = [{period:{start:'2024-04-01',end:'2024-04-07'},citations:[citation]}];
  s.result.findings[0].citations.push(citation);
  s.result.snapshot.selected_versions[dated.document.source_id] = dated.document.version;
  await page.route(`${s.root}/assessments/selection-browser-run/sources/${dated.document.document_version_id}`,
    route => route.fulfill({json:dated}));
  await s.selection.getByRole('button',{name:'Run selected assessment with live model',exact:true}).click();
  await page.getByRole('region',{name:'Assessment result',exact:true}).getByRole('button',
    {name:`Inspect ${record.location}`,exact:true}).first().click();
  const source = page.getByRole('dialog',{name:'Assessment source',exact:true});
  await expect(source).toContainText('Stated evidence periods');
  await expect(source).toContainText('2024-04-01 to 2024-04-07');
  await expect(source).toContainText(record.location);
  await expect(source).toContainText('These dates do not establish complete records or actual control operation.');
  await source.screenshot({path:`${evidence}/period-source-desktop.png`});
  await page.getByRole('button',{name:'Close source',exact:true}).click();
  dated.stated_periods = [];
  await page.getByRole('region',{name:'Assessment result',exact:true}).getByRole('button',
    {name:`Inspect ${record.location}`,exact:true}).first().click();
  await expect(source).toContainText('Stated evidence period: Unknown');
});

// Browser conformance uses controlled responses. These checks never dispatch Bedrock.
async function setup(page: Page, state = 'completed') {
  await page.goto('/');
  await page.getByRole('button', {name: 'Continue with local identity'}).click();
  await page.getByLabel('Fictional bank name').fill(`Fictional selection bank ${Date.now()}`);
  await page.getByLabel('I confirm this case contains fictional data only.', {exact:true}).check();
  await page.getByRole('button', {name:'Save fictional case'}).click();
  await page.getByLabel('Document file', {exact:true}).setInputFiles({name:'custom-fiction.txt', mimeType:'text/plain',
    buffer:Buffer.from('FICTIONAL DATA ONLY\nThe control requires access-log review. Owner and frequency are not stated.')});
  await page.getByLabel('I confirm this document contains fictional data only.', {exact:true}).check();
  await page.getByRole('button', {name:'Upload fictional document',exact:true}).click();
  await expect(page.getByRole('button', {name:/custom-fiction.txt/}).first()).toBeVisible();
  const config = await (await page.request.get('/config.json')).json();
  const caseId = new URL(page.url()).searchParams.get('case')!;
  const root = `${config.api_url}/api/cases/${caseId}`;
  const catalog = await (await page.request.get(`${root}/assessment-selection`)).json();
  const bank = catalog.sources.find((s:any) => s.document.kind === 'policy');
  const regulatory = catalog.sources.find((s:any) => s.document.kind === 'regulation');
  const clauses = catalog.obligations.slice(0, 2);
  const citation = (source:any, passage:any) => ({document_version_id:source.document.document_version_id,
    passage_id:passage.passage_id, location:passage.location, quote:passage.text});
  const requirements = clauses.map((c:any) => ({obligation_id:c.obligation_id, requirement:`Selected requirement ${c.label}`,
    applicability:'Applicability needs review.', conditions:['Selected condition.'], exceptions:['Selected exception.'],
    citations:[citation(regulatory, regulatory.passages.find((p:any) => p.passage_id === c.scope_passage_ids.at(-1)))]}));
  const bankCitation = citation(bank, bank.passages[0]);
  const findings = requirements.map((o:any, i:number) => ({finding_id:`selection-finding-${i}`, obligation_id:o.obligation_id,
    control_ids:['selected-control'], status:'needs_review', evidence_condition:'missing', gap_kind:'evidence',
    rationale:`Original selected finding ${i}.`, primary_recommendation:`Request dated records for finding ${i}.`,
    citations:[...o.citations, bankCitation], claims:[{obligation_element:o.requirement, reason:'Activity records are missing.',
      operational:true, evidence_period:null, citations:[bankCitation], examined_exceptions:[], conflicting_evidence:[]}]}));
  const result:any = {job:{job_id:'selection-browser-run', state, model_calls:state === 'queued' ? 0 : 7,
      stop_reason:state === 'partial' ? 'model_failure' : null,
      unchecked_obligations:state === 'completed' ? [] : [clauses[1].obligation_id]},
    snapshot:{snapshot_id:'selection-browser-snapshot', case_id:caseId, assessment_date:'2024-04-08',
      selected_obligations:clauses.map((c:any) => c.obligation_id),model_version:'in.openai.gpt-5.6-luna',prompt_version:'assessment-vs5-selected-v1',
      selected_versions:{[regulatory.document.source_id]:regulatory.document.version, [bank.document.source_id]:bank.document.version}},
    data_mode:'synthetic_live', freshness:'unverified', live_model_calls:(state === 'queued' ? 0 : 7) as number | null, cost_usd:null,
    obligations:requirements, obligation:requirements[0], controls:[{control_id:'selected-control', statement:'Selected bank control.',
      owner:null, frequency:null, citations:[bankCitation]}], control:null,
    findings:state === 'queued' ? [] : state === 'partial' ? findings.slice(0,1) : findings,
    reviews:[], summary:{cutoff:'2026-10-11T00:00:00Z', eligible:state === 'queued' ? 0 : state === 'partial' ? 1 : 2,
      reviewed:0, approved:0, edited:0, rejected:0, pending:state === 'completed' ? 2 : state === 'partial' ? 1 : 0,
      approval_rate:null, edit_rate:null, rejection_rate:null, adoption_rate:null, review_coverage:null}, trace:{attempts:[]}};
  await page.route(`${root}/assessments/selection-browser-run`, route => route.fulfill({json:result}));
  await page.route(`${root}/assessments/selected`, route => route.fulfill({status:202,json:{job_id:result.job.job_id}}));
  const selection = page.getByRole('region',{name:'Selected historical assessment',exact:true});
  const choose = async () => {
    await selection.getByLabel('custom-fiction.txt · Version 1', {exact:true}).check();
    for (const clause of clauses) await selection.getByLabel(clause.label,{exact:true}).check();
    await selection.getByLabel('Assessment date',{exact:true}).fill('2024-04-08');
  };
  return {root, caseId, catalog, bank, regulatory, clauses, result, selection, choose};
}

test('LD-B01 OpenAI local demo identifies its provider and metadata-only Langfuse configuration', async ({page}) => {
  const s=await setup(page);
  await page.route(`${s.root}/assessment-selection`,route=>route.fulfill({json:{...s.catalog,
    model_id:'openai:gpt-4.1-mini-2025-04-14',demo_services:{openai_key_configured:true,langfuse_configured:true}}}));
  await page.reload();
  await page.getByRole('button',{name:'Continue with local identity',exact:true}).click();
  const selection=page.getByRole('region',{name:'Selected historical assessment',exact:true});
  await expect(selection).toContainText('OpenAI local demo');
  await expect(selection).toContainText('gpt-4.1-mini-2025-04-14');
  await expect(selection).toContainText('metadata only');
  await expect(selection).toContainText('Private bank data is not permitted');
  await expect(selection).not.toContainText('AWS model access is required');
});

test('LD-B02 a late catalog response cannot remove a newly uploaded policy', async ({page}) => {
  let release!: () => void;
  const gate=new Promise<void>(resolve=>{release=resolve;});
  let first=true;
  await page.route('**/assessment-selection',async route=>{
    const response=await route.fetch();
    if(first){first=false;await gate;}
    await route.fulfill({response});
  });
  const s=await setup(page);
  const policy=page.getByLabel('Policy version',{exact:true});
  await expect(policy.locator('option')).toContainText(['custom-fiction.txt']);
  const finished=page.waitForResponse(response=>response.url().endsWith('/assessment-selection'));
  release(); await finished;
  await page.evaluate(()=>new Promise<void>(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve()))));
  await expect(policy.locator('option')).toContainText(['custom-fiction.txt']);
  await expect(page.getByRole('button',{name:'Run controlled assessment',exact:true})).toBeEnabled();
});

test('LD-B03 missing OpenAI key prevents starting a live demo from the interface', async ({page}) => {
  const s=await setup(page);
  await page.route(`${s.root}/assessment-selection`,route=>route.fulfill({json:{...s.catalog,
    model_id:'openai:gpt-4.1-mini-2025-04-14',demo_services:{openai_key_configured:false,langfuse_configured:false}}}));
  await page.reload(); await page.getByRole('button',{name:'Continue with local identity',exact:true}).click();
  await expect(s.selection).toContainText('OpenAI key: Missing'); await s.choose();
  await expect(s.selection.getByRole('button',{name:'Run selected assessment with live model',exact:true})).toBeDisabled();
});

test('VS5-SB01 real catalog and arbitrary upload produce exact selected admission', async ({page}) => {
  const s = await setup(page);
  await s.choose();
  await expect(s.selection).toContainText('Saved historical excerpts');
  await expect(s.selection).toContainText('Current status unverified');
  await expect(s.selection).toContainText(s.regulatory.document.effective_date);
  const sent = page.waitForRequest(`${s.root}/assessments/selected`);
  await s.selection.getByRole('button',{name:'Run selected assessment with live model',exact:true}).click();
  const body = (await sent).postDataJSON();
  expect(body.selected_versions).toEqual(s.result.snapshot.selected_versions);
  expect(body.selected_obligations).toEqual(s.clauses.map((c:any) => c.obligation_id));
  expect(body.assessment_date).toBe('2024-04-08');
  expect(body.mode).toBe('historical');
  expect(Object.keys(body).sort()).toEqual(['assessment_date','idempotency_key','mode','selected_obligations','selected_versions']);
  const result = page.getByRole('region',{name:'Assessment result',exact:true});
  await expect(result).toContainText('Fictional inputs · Live model processing');
  await expect(result).toContainText('Owner: Unknown');
  await expect(result).toContainText('Frequency: Unknown');
  await expect(result).toContainText('Evidence period: Unknown');
});

test('VS5-SB02 queued selected run shows scope and recorded counters without a finding', async ({page}) => {
  const s = await setup(page,'queued'); await s.choose();
  await s.selection.getByRole('button',{name:'Run selected assessment with live model',exact:true}).click();
  const result = page.getByRole('region',{name:'Assessment result',exact:true});
  await expect(result).toContainText('Assessment queued');
  await expect(result).toContainText(s.clauses[1].obligation_id);
  await result.getByText('Saved run record',{exact:true}).click();
  await expect(result).toContainText('Live model calls: 0');
  await expect(result).not.toContainText('Controlled dispatches');
  await expect(result).toContainText('Cost: Unknown');
});

test('VS5-SB03 each selected finding uses its own citations and review revision', async ({page}) => {
  const s = await setup(page); await s.choose();
  s.result.reviews.push({event_id:'earlier-review',finding_id:'selection-finding-0',event_kind:'final_review',
    disposition:'approved',revision:2,reason:null,accepted_content:null,committed_at:'2026-10-10T00:00:00Z'});
  await page.route(`${s.root}/assessments/selection-browser-run/findings/*/reviews`, async route => {
    const id = route.request().url().split('/').at(-2)!;
    const body = route.request().postDataJSON();
    const own = s.result.reviews.filter((r:any) => r.finding_id === id);
    expect(body.expected_revision).toBe(own.at(-1)?.revision || 0);
    s.result.reviews.push({...body,finding_id:id,event_id:`review-${id}`,revision:body.expected_revision+1,
      committed_at:'2026-10-11T00:00:00Z'});
    await route.fulfill({json:s.result.reviews.at(-1)});
  });
  await page.route(`${s.root}/assessments/selection-browser-run/sources/${s.bank.document.document_version_id}`,
    route => route.fulfill({json:s.bank}));
  await s.selection.getByRole('button',{name:'Run selected assessment with live model',exact:true}).click();
  const result = page.getByRole('region',{name:'Assessment result',exact:true});
  await result.getByLabel('Finding',{exact:true}).selectOption('selection-finding-1');
  await expect(result.locator('.original-rationale')).toHaveText('Original selected finding 1.');
  await expect(result.getByRole('region',{name:'Selected finding review history',exact:true})).not.toContainText('Revision 2');
  await result.getByRole('button',{name:`Inspect ${s.bank.passages[0].location}`,exact:true}).click();
  await expect(page.getByRole('dialog',{name:'Assessment source',exact:true})).toContainText(s.bank.document.document_version_id);
  await page.getByRole('button',{name:'Close source',exact:true}).click();
  await result.getByRole('button',{name:'Save review',exact:true}).click();
  await expect(result.getByRole('region',{name:'Selected finding review history',exact:true})).toContainText('Revision 1');
  await result.getByLabel('Finding',{exact:true}).selectOption('selection-finding-0');
  await expect(result.locator('.original-rationale')).toHaveText('Original selected finding 0.');
  await result.getByRole('button',{name:'Save review',exact:true}).click();
  await expect(result.getByRole('region',{name:'Selected finding review history',exact:true})).toContainText('Revision 3');
});

test('VS5-SB04 uncertain selected admission keeps scope and retry identity', async ({page}) => {
  const s = await setup(page); await s.choose();
  await page.route(`${s.root}/assessments/selected`,route => route.fulfill({status:503,json:{message:'Admission could not be confirmed.'}}),{times:1});
  const sent = page.waitForRequest(`${s.root}/assessments/selected`);
  const run = s.selection.getByRole('button',{name:'Run selected assessment with live model',exact:true});
  await run.click(); const first = (await sent).postDataJSON();
  await expect(page.getByRole('alert')).toContainText('Admission could not be confirmed');
  await expect(run).toBeDisabled();
  await page.getByRole('button',{name:'Refresh assessment',exact:true}).click();
  await expect(run).toBeEnabled();
  await expect(s.selection.getByLabel('custom-fiction.txt · Version 1',{exact:true})).toBeChecked();
  const retried = page.waitForRequest(`${s.root}/assessments/selected`); await run.click();
  expect((await retried).postDataJSON()).toEqual(first);
});

test('VS5-SB05 mobile keyboard selection keeps historical verification limits visible', async ({page}) => {
  await page.setViewportSize({width:390,height:844});
  const s = await setup(page); await s.choose();
  await expect(s.selection).toContainText('Current assessments are unavailable');
  const run = s.selection.getByRole('button',{name:'Run selected assessment with live model',exact:true});
  await run.focus(); await page.keyboard.press('Enter');
  await expect(page.getByRole('region',{name:'Assessment result',exact:true})).toContainText('Original selected finding 0.');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await s.selection.screenshot({path:`${evidence}/selection-setup-mobile.png`});
  await page.screenshot({path:`${evidence}/selection-mobile.png`,fullPage:true});
});

test('VS5-SB06 partial live result retains findings and exact unchecked scope', async ({page}) => {
  const s = await setup(page,'partial'); await s.choose();
  s.result.trace.attempts.push({event_id:'recorded-attempt',stage:'model_call',state:'succeeded',duration_seconds:0.1,
    usage:{input_tokens:123,output_tokens:9}});
  await s.selection.getByRole('button',{name:'Run selected assessment with live model',exact:true}).click();
  const result = page.getByRole('region',{name:'Assessment result',exact:true});
  await expect(result).toContainText('Original selected finding 0.');
  await expect(result).toContainText('model failure');
  await expect(result).toContainText(s.clauses[1].obligation_id);
  await result.getByText('Saved run record',{exact:true}).click();
  await expect(result).toContainText('Live model calls: 7');
  await expect(result).toContainText('Input tokens: 123');
  await expect(result).toContainText('Output tokens: 9');
  await expect(result).not.toContainText('Live model calls: 0');
  await page.screenshot({path:`${evidence}/selection-partial.png`,fullPage:true});
});

test('VS5-CRB01 incomplete dispatch audit shows Unknown without inventing zero calls', async ({page}) => {
  const s = await setup(page,'partial'); await s.choose();
  s.result.live_model_calls = null;
  await s.selection.getByRole('button',{name:'Run selected assessment with live model',exact:true}).click();
  const result = page.getByRole('region',{name:'Assessment result',exact:true});
  await result.getByText('Saved run record',{exact:true}).click();
  await expect(result).toContainText('Live model calls: Unknown');
  await expect(result).not.toContainText('Live model calls: 0');
});

test('VS5-SB07 a replacement selection keeps one version per source', async ({page}) => {
  const s = await setup(page); await s.choose();
  await page.getByLabel('Replace source',{exact:true}).selectOption(s.bank.document.source_id);
  await page.getByLabel('Document file',{exact:true}).setInputFiles({name:'custom-fiction.txt',mimeType:'text/plain',
    buffer:Buffer.from('FICTIONAL DATA ONLY\nReplacement policy. Its operational records are still missing.')});
  await page.getByLabel('I confirm this document contains fictional data only.',{exact:true}).check();
  await page.getByRole('button',{name:'Upload fictional document',exact:true}).click();
  const first = s.selection.getByLabel('custom-fiction.txt · Version 1',{exact:true});
  const second = s.selection.getByLabel('custom-fiction.txt · Version 2',{exact:true});
  await second.check(); await expect(first).not.toBeChecked();
  await expect(second).toBeChecked(); await expect(s.selection).toContainText('Selected: 2 documents · 2 clauses');
  s.result.snapshot.selected_versions[s.bank.document.source_id] = '2';
  const request = page.waitForRequest(`${s.root}/assessments/selected`);
  await s.selection.getByRole('button',{name:'Run selected assessment with live model',exact:true}).click();
  expect((await request).postDataJSON().selected_versions).toEqual(s.result.snapshot.selected_versions);
});
