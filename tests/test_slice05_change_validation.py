"""Specified pairs and hostile interpretations. No provider, model call, or AWS traffic."""
import copy
import hashlib
import unittest

from regulatory_agent.contracts import ContractError, Snapshot
from regulatory_agent.regulatory_changes import prepare_pair, validate_changes


class ChangeValidationTests(unittest.TestCase):
    def setUp(self):
        self.old_raw=b'Historical test rule: review access weekly.'
        self.new_raw=b'Historical test rule: review access weekly with independent approval.'
        self.older=self.source('older',self.old_raw,'2023-01-01','2023-04-01')
        self.newer=self.source('newer',self.new_raw,'2024-01-01','2024-04-01')
        self.snapshot=Snapshot(snapshot_id='baseline',case_id='case-a',bank_profile={'name':'Fictional bank'},
            selected_versions={'RBI-TEST':'older','bank':'1'},selected_document_ids={'RBI-TEST':'older','bank':'bank-1'},
            selected_obligations=['rule-a','rule-b'],assessment_date='2024-05-01',mode='historical',
            prompt_version='assessment-vs5-selected-period-v1',model_version='in.openai.gpt-5.6-luna',synthetic=True)
        self.findings=[{'snapshot_id':'baseline','obligation_id':'rule-a','control_ids':['ACCESS-01']},
                       {'snapshot_id':'baseline','obligation_id':'rule-b','control_ids':['BACKUP-01']}]

    def source(self, identity, raw, publication, effective):
        return {'document':{'document_version_id':identity,'case_id':'case-a','source_id':'RBI-TEST',
            'kind':'regulation','version':identity,'sha256':hashlib.sha256(raw).hexdigest(),
            'storage_reference':identity+'-original','synthetic':False,
            'source_url':'https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=1',
            'publication_date':publication,'effective_date':effective},
            'authority':'Reserve Bank of India','freshness':'unverified',
            'passages':[{'document_version_id':identity,'passage_id':identity+'-p1',
                         'location':'Clause 1','text':raw.decode()}]}

    def pair(self):
        return prepare_pair(self.snapshot,self.older,self.newer,self.old_raw,self.new_raw)

    def citation(self, source):
        passage=source['passages'][0]
        return {k:passage[k] for k in ('document_version_id','passage_id','location')}|{'quote':passage['text']}

    def obligation(self, identity, source):
        return {'obligation_id':identity,'requirement':source['passages'][0]['text'],
            'conditions':['Privileged access'],'exceptions':[],'applicability':'Fictional commercial bank',
            'citations':[self.citation(source)]}

    def reply(self):
        changes=[]
        for identity in self.snapshot.selected_obligations:
            changes.append({'obligation_id':identity,'kind':'changed_requirement',
                'before':self.obligation(identity,self.older),'after':self.obligation(identity,self.newer),
                'reason':'The newer rule adds independent approval.',
                'basis':[self.citation(self.older),self.citation(self.newer)],
                'affected_control_ids':['ACCESS-01' if identity=='rule-a' else 'BACKUP-01']})
        return {'snapshot_id':'baseline','older_version_id':'older','newer_version_id':'newer','changes':changes}

    def test_vc01_context_keeps_exact_pair_selected_scope_and_independent_dates(self):
        pair=self.pair()
        self.assertEqual(pair['selected_obligations'],['rule-a','rule-b'])
        self.assertEqual(pair['older_source']['passages'],self.older['passages'])
        self.assertEqual(pair['newer_source']['document'],self.newer['document'])
        self.assertEqual(pair['metadata_changes']['effective_date'],{'older':'2023-04-01','newer':'2024-04-01'})
        self.assertEqual(pair['assessment_date'],'2024-05-01')
        self.assertEqual(pair['freshness'],'unverified')
        self.assertNotIn('older_original',pair);self.assertNotIn('newer_original',pair)

    def test_vc02_changed_requirements_keep_citations_and_only_baseline_mappings(self):
        result=validate_changes(self.pair(),self.reply(),self.findings)
        self.assertTrue(result['assessment_required']); self.assertTrue(result['selection_review_required'])
        self.assertEqual(result['affected_control_ids'],['ACCESS-01','BACKUP-01'])
        self.assertEqual(result['changes'][0]['before']['citations'],[self.citation(self.older)])
        self.assertEqual(result['changes'][0]['after']['conditions'],['Privileged access'])

    def test_vc03_wrong_case_source_selection_identical_or_reversed_pair_fails(self):
        for side,field,value in [('older','case_id','other'),('newer','case_id','other'),
                ('newer','source_id','OTHER'),('older','kind','policy'),('older','version','not-selected'),
                ('newer','document_version_id','older'),('newer','version','older'),
                ('newer','publication_date','2022-01-01')]:
            old,new=copy.deepcopy(self.older),copy.deepcopy(self.newer)
            (old if side=='older' else new)['document'][field]=value
            with self.subTest(side=side,field=field),self.assertRaises(ContractError):
                prepare_pair(self.snapshot,old,new,self.old_raw,self.new_raw)

    def test_vc04_original_hash_metadata_and_authority_are_trust_boundaries(self):
        with self.assertRaises(ContractError):prepare_pair(self.snapshot,self.older,self.newer,b'changed',self.new_raw)
        for change in ({'effective_date':'2099-01-01'},{'authority':'Unverified intermediary'}):
            new=copy.deepcopy(self.newer);new.update(change)
            with self.subTest(change=change),self.assertRaises(ContractError):
                prepare_pair(self.snapshot,self.older,new,self.old_raw,self.new_raw)
        for url in ('https://rbi.org.in.evil.test/rule','https://user:password@rbi.org.in/rule','https://rbi.org.in:8443/rule'):
            new=copy.deepcopy(self.newer);new['document']['source_url']=url
            with self.subTest(url=url),self.assertRaises(ContractError):
                prepare_pair(self.snapshot,self.older,new,self.old_raw,self.new_raw)

    def test_vc05_duplicate_wrong_version_and_over_limit_context_never_truncate(self):
        for change in ('duplicate','wrong-version','too-many','too-large'):
            new=copy.deepcopy(self.newer);raw=self.new_raw
            if change=='duplicate':new['passages']*=2
            elif change=='wrong-version':new['passages'][0]['document_version_id']='older'
            elif change=='too-many':new['passages']=[new['passages'][0]|{'passage_id':f'newer-{n}'} for n in range(20)]
            else:
                raw=b'x'*64_000;new['passages'][0]['text']=raw.decode()
                new['document']['sha256']=hashlib.sha256(raw).hexdigest()
            with self.subTest(change=change),self.assertRaises(ContractError) as caught:
                prepare_pair(self.snapshot,self.older,new,self.old_raw,raw)
            if change in {'too-many','too-large'}:self.assertEqual(str(caught.exception),'comparison_context_limit')

    def test_vc06_forged_pair_and_unselected_or_missing_obligations_fail(self):
        for field,value in [('snapshot_id','other'),('older_version_id','other'),('newer_version_id','other')]:
            reply=self.reply();reply[field]=value
            with self.subTest(field=field),self.assertRaises(ContractError):validate_changes(self.pair(),reply,self.findings)
        for change in ('omit','duplicate','extra'):
            reply=self.reply()
            if change=='omit':reply['changes'].pop()
            elif change=='duplicate':reply['changes'][1]=copy.deepcopy(reply['changes'][0])
            else:reply['changes'].append(reply['changes'][0]|{'obligation_id':'unselected'})
            with self.subTest(change=change),self.assertRaises(ContractError):validate_changes(self.pair(),reply,self.findings)

    def test_vc07_every_reference_resolves_to_its_exact_side_location_and_quote(self):
        for change in ('wrong-side','missing-side','invented','location','quote','blank'):
            reply=self.reply();item=reply['changes'][0]
            if change=='wrong-side':item['before']['citations']=[self.citation(self.newer)]
            elif change=='missing-side':item['basis']=[self.citation(self.older)]
            else:
                citation=item['basis'][0]
                if change=='invented':citation['passage_id']='invented'
                elif change=='location':citation['location']='Clause 999'
                elif change=='quote':citation['quote']='No approval is necessary.'
                else:citation['quote']=' '
            with self.subTest(change=change),self.assertRaises(ContractError):validate_changes(self.pair(),reply,self.findings)

    def test_vc08_affected_controls_cannot_be_invented_or_borrowed_from_another_mapping(self):
        for controls in (['INVENTED'],['BACKUP-01'],['ACCESS-01','ACCESS-01']):
            reply=self.reply();reply['changes'][0]['affected_control_ids']=controls
            with self.subTest(controls=controls),self.assertRaises(ContractError):validate_changes(self.pair(),reply,self.findings)
        for kind in ('unchanged','wording_only','appearance_only','undetermined'):
            reply=self.reply();reply['changes'][0]['kind']=kind
            with self.subTest(kind=kind),self.assertRaises(ContractError):validate_changes(self.pair(),reply,self.findings)
        findings=copy.deepcopy(self.findings);findings[0]['snapshot_id']='other'
        with self.assertRaises(ContractError):validate_changes(self.pair(),self.reply(),findings)

    def test_vc09_classifications_keep_required_before_after_conditions_and_exceptions(self):
        for kind,side in [('added_requirement','before'),('withdrawn_requirement','after'),('changed_requirement','before')]:
            reply=self.reply();reply['changes'][0]['kind']=kind
            if kind=='changed_requirement':reply['changes'][0][side]=None
            with self.subTest(kind=kind),self.assertRaises(ContractError):validate_changes(self.pair(),reply,self.findings)
        for field in ('conditions','exceptions','applicability'):
            reply=self.reply();item=reply['changes'][0];item['kind']='wording_only';item['affected_control_ids']=[]
            item['after'][field]='Other banks' if field=='applicability' else ['Except weekends']
            with self.subTest(field=field),self.assertRaises(ContractError):validate_changes(self.pair(),reply,self.findings)
        reply=self.reply();reply['changes'][0]['after']['obligation_id']='rule-b'
        with self.assertRaises(ContractError):validate_changes(self.pair(),reply,self.findings)

    def test_vc10_future_effective_change_needs_selection_review_without_earlier_assessment(self):
        self.newer['document']['effective_date']='2025-01-01'
        result=validate_changes(self.pair(),self.reply(),self.findings)
        self.assertFalse(result['assessment_required']);self.assertTrue(result['selection_review_required'])
        self.assertFalse(self.pair()['newer_applicable'])

    def test_vc11_withdrawal_and_unknown_metadata_keep_evidence_and_uncertainty(self):
        reply=self.reply();reply['changes'][0]['kind']='withdrawn_requirement';reply['changes'][0]['after']=None
        result=validate_changes(self.pair(),reply,self.findings)
        self.assertEqual(result['changes'][0]['basis'][1],self.citation(self.newer))
        pair=self.pair();self.assertIsNone(pair['newer_source']['withdrawn']);self.assertIsNone(pair['newer_source']['amendments'])
        for item in reply['changes']:
            item.update(kind='undetermined',before=None,after=None,affected_control_ids=[])
        result=validate_changes(pair,reply,self.findings)
        self.assertFalse(result['assessment_required']);self.assertTrue(result['selection_review_required'])
        self.assertEqual(result['unresolved_obligation_ids'],['rule-a','rule-b'])

    def test_vc12_preparation_and_validation_do_not_mutate_saved_inputs(self):
        reply=self.reply();saved=copy.deepcopy((self.older,self.newer,self.snapshot.model_dump(),self.findings,reply))
        pair=self.pair();before=copy.deepcopy(pair)
        validate_changes(pair,reply,self.findings)
        self.assertEqual(pair,before)
        self.assertEqual((self.older,self.newer,self.snapshot.model_dump(),self.findings,reply),saved)

    def test_vc13_unchanged_wording_appearance_and_added_requirements_keep_their_meanings(self):
        for kind,text in (('unchanged',self.old_raw),('wording_only',b'Historical test rule: weekly review of access.'),
                          ('appearance_only',b'Historical test rule: review access weekly!')):
            self.new_raw=text;self.newer=self.source('newer',text,'2024-01-01','2024-04-01')
            reply=self.reply()
            for item in reply['changes']:item.update(kind=kind,affected_control_ids=[])
            result=validate_changes(self.pair(),reply,self.findings)
            self.assertFalse(result['assessment_required']);self.assertEqual(result['affected_control_ids'],[])
        reply=self.reply();reply['changes'][0].update(kind='added_requirement',before=None)
        self.assertTrue(validate_changes(self.pair(),reply,self.findings)['assessment_required'])

    def test_vc14_shared_assessment_citations_reject_whitespace_only_quotes(self):
        from regulatory_agent.assessment_pipeline import AssessmentPipeline
        from regulatory_agent.contracts import Citation
        check=object.__new__(AssessmentPipeline)
        quote=Citation.model_validate(self.citation(self.older)|{'quote':' '})
        with self.assertRaises(ContractError):check._check_citations([quote],self.older['passages'])

    def test_vc15_unchanged_classification_cannot_hide_a_changed_requirement_statement(self):
        reply=self.reply();reply['changes'][0].update(kind='unchanged',affected_control_ids=[])
        with self.assertRaises(ContractError):validate_changes(self.pair(),reply,self.findings)


if __name__=='__main__':unittest.main()
