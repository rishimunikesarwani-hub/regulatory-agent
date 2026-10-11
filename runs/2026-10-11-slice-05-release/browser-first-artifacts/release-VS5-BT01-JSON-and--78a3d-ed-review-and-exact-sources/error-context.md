# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: release.spec.ts >> VS5-BT01 JSON and Markdown downloads preserve saved review and exact sources
- Location: tests\release.spec.ts:25:1

# Error details

```
Error: expect(received).toContain(expected) // indexOf

Expected substring: "Clause 19(b)"
Received string:    "# The Regulator assessment report·
## Export status·
> Assessment export · Simulated processing · Fictional bank data·
## Snapshot and selected versions·
> \\{
>   \"assessment\\_date\": \"2024-04-08\",
>   \"bank\\_profile\": \\{
>     \"name\": \"Fictional export bank 1791689797588\"
>   \\},
>   \"case\\_id\": \"41d7ddeee1f545419a5999f50dad0e74\",
>   \"mode\": \"historical\",
>   \"model\\_version\": \"in.openai.gpt-5.6-luna\",
>   \"prompt\\_version\": \"controlled-vs3-v1\",
>   \"selected\\_obligations\": \\[
>     \"RBI-IT-19b\"
>   \\],
>   \"selected\\_versions\": \\{
>     \"03562af9a8484489ac3d8d3343c208d1\": \"1\",
>     \"RBI-IT-2023\": \"2023-11-07\"
>   \\},
>   \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>   \"synthetic\": true
> \\}·
## Observed job state·
> \\{
>   \"authority\\_verified\\_at\": null,
>   \"case\\_id\": \"41d7ddeee1f545419a5999f50dad0e74\",
>   \"created\\_at\": 1791689798.207341,
>   \"deadline\": 1791690398.2572968,
>   \"finished\\_at\": 1791689798.4621043,
>   \"freshness\": \"unverified\",
>   \"job\\_id\": \"5f4c830275aa4855a0d52df82efe8cec\",
>   \"label\": \"Simulated\",
>   \"lease\\_until\": 1791689828.446662,
>   \"model\\_calls\": 1,
>   \"retrieval\\_calls\": 0,
>   \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>   \"stage\": \"persistence\",
>   \"started\\_at\": 1791689798.2572968,
>   \"state\": \"completed\",
>   \"stop\\_reason\": null,
>   \"unchecked\\_obligations\": \\[\\]
> \\}·
## Report cutoff·
> 2026-10-11T03:36:39.074540\\+00:00·
## Freshness and authority verification·
> \\{
>   \"freshness\": \"unverified\",
>   \"authority\\_verified\\_at\": null
> \\}·
## Obligation·
> \\{
>   \"obligation\\_id\": \"RBI-IT-19b\",
>   \"requirement\": \"Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed.\",
>   \"conditions\": \\[
>     \"Personnel with elevated system access entitlements.\",
>     \"Applicability to the listed regulated entities must be established.\"
>   \\],
>   \"exceptions\": \\[
>     \"Local Area Banks\",
>     \"NBFC-Core Investment Companies\"
>   \\],
>   \"applicability\": \"Unverified for this fictional bank profile.\",
>   \"citations\": \\[
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:19b\",
>       \"location\": \"Clause 19\\(b\\)\",
>       \"quote\": \"Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed.\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:2ai\",
>       \"location\": \"Clause 2\\(a\\)\\(i\\)\",
>       \"quote\": \"all Banking Companies 1 , Corresponding New Banks and State Bank of India as defined under subsections \\(c\\), \\(da\\) and \\(nc\\) of section 5 of the Banking Regulation Act, 1949 \\(collectively referred to as ‘commercial banks’ hereinafter\\).\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:2b\",
>       \"location\": \"Clause 2\\(b\\)\",
>       \"quote\": \"These Directions shall not be applicable to: Local Area Banks NBFC-Core Investment Companies\"
>     \\}
>   \\]
> \\}·
## Mapped control·
> \\{
>   \"control\\_id\": \"ACCESS-01\",
>   \"statement\": \"Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.\",
>   \"purpose\": \"Privileged session oversight\",
>   \"owner\": null,
>   \"frequency\": \"Weekly under the fictional bank policy.\",
>   \"citations\": \\[
>     \\{
>       \"document\\_version\\_id\": \"9999fb6aa81340eca0424f137a044417\",
>       \"passage\\_id\": \"9999fb6aa81340eca0424f137a044417-2\",
>       \"location\": \"Line 2\",
>       \"quote\": \"Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.\"
>     \\}
>   \\]
> \\}·
## Original findings and recommendation IDs·
> \\[
>   \\{
>     \"finding\\_id\": \"902930fe73765e8ab5b6e53e7be8b3af\",
>     \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>     \"obligation\\_id\": \"RBI-IT-19b\",
>     \"control\\_ids\": \\[
>       \"ACCESS-01\"
>     \\],
>     \"status\": \"needs\\_review\",
>     \"evidence\\_condition\": \"missing\",
>     \"citations\": \\[
>       \\{
>         \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>         \"passage\\_id\": \"RBI-IT-2023:2023-11-07:19b\",
>         \"location\": \"Clause 19\\(b\\)\",
>         \"quote\": \"Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed.\"
>       \\},
>       \\{
>         \"document\\_version\\_id\": \"9999fb6aa81340eca0424f137a044417\",
>         \"passage\\_id\": \"9999fb6aa81340eca0424f137a044417-2\",
>         \"location\": \"Line 2\",
>         \"quote\": \"Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.\"
>       \\}
>     \\],
>     \"rationale\": \"Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.\",
>     \"remedy\": \"Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.\",
>     \"gap\\_kind\": \"evidence\",
>     \"applicability\\_reason\": null,
>     \"run\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>     \"primary\\_recommendation\": \"Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.\",
>     \"available\\_at\": \"2026-10-11T03:36:38.428757Z\",
>     \"model\\_id\": \"in.openai.gpt-5.6-luna\",
>     \"prompt\\_version\": \"controlled-vs3-v1\",
>     \"data\\_mode\": \"controlled\\_simulation\",
>     \"source\\_version\\_ids\": \\[
>       \"03562af9a8484489ac3d8d3343c208d1:1\",
>       \"RBI-IT-2023:2023-11-07\"
>     \\]
>   \\}
> \\]·
## Saved review events·
> \\[
>   \\{
>     \"event\\_kind\": \"final\\_review\",
>     \"disposition\": \"approved\",
>     \"accepted\\_content\": \\{
>       \"status\": \"needs\\_review\",
>       \"rationale\": \"Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.\",
>       \"recommendation\": \"Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.\"
>     \\},
>     \"reason\": null,
>     \"expected\\_revision\": 0,
>     \"idempotency\\_key\": \"8f8931d9-f276-417f-9b30-4b5dc8058c99\",
>     \"event\\_id\": \"a9a08f9c0d2d488ca782a51298cf3d3a\",
>     \"finding\\_id\": \"902930fe73765e8ab5b6e53e7be8b3af\",
>     \"reviewer\\_id\": \"slice-05-tests\",
>     \"committed\\_at\": \"2026-10-11T03:36:39.041402Z\",
>     \"revision\": 1
>   \\}
> \\]·
## Review summary·
metric_definition_version: d24-v1·
cutoff: 2026-10-11T03:36:39.074540+00:00·
data_mode: controlled_simulation·
run_id: 13d0f2d9f7ec559f910f8c2d84b82c94·
eligible: 1·
reviewed: 1·
pending: 0·
approved: 1·
edited: 0·
rejected: 0·
approval_rate: 1.0·
edit_rate: 0.0·
rejection_rate: 0.0·
adoption_rate: 1.0·
review_coverage: 1.0·
## Recorded runtime·
cost: Unknown·
> \\{
>   \"run\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>   \"attempts\": \\[
>     \\{
>       \"actual\\_response\\_model\\_id\": null,
>       \"artifact\\_ids\": \\[\\],
>       \"attempt\\_id\": \"70c88438125848eab1679ad107559be9\",
>       \"candidate\\_passage\\_ids\": \\[\\],
>       \"dispatched\": true,
>       \"duration\\_seconds\": 0.0,
>       \"errors\": \\[\\],
>       \"event\\_id\": \"04c92ffc0949481d876b7cb438656340\",
>       \"finished\\_at\": \"2026-10-11T03:36:38.404635Z\",
>       \"first\\_token\\_seconds\": null,
>       \"job\\_id\": \"5f4c830275aa4855a0d52df82efe8cec\",
>       \"model\\_id\": null,
>       \"operation\": \"internal\",
>       \"original\\_processing\\_event\\_id\": null,
>       \"provider\\_request\\_id\": null,
>       \"retry\\_index\": 0,
>       \"returned\\_bytes\": null,
>       \"run\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"selected\\_passage\\_ids\": \\[\\],
>       \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"stage\": \"validation\",
>       \"stage\\_id\": \"validation\",
>       \"started\\_at\": \"2026-10-11T03:36:38.404635Z\",
>       \"state\": \"succeeded\",
>       \"streaming\": false,
>       \"unused\\_allowance\": null,
>       \"usage\": \\{
>         \"cache\\_read\\_tokens\": null,
>         \"cache\\_write\\_tokens\": null,
>         \"input\\_tokens\": null,
>         \"output\\_tokens\": null
>       \\},
>       \"versions\": \\{
>         \"application\": \"vs4-v1\",
>         \"chunking\": \"source-locations-v1\",
>         \"extraction\": \"vs2-v1\",
>         \"model\\_configuration\": \"controlled-response-v1\",
>         \"prompt\": \"controlled-vs3-v1\",
>         \"retrieval\": \"fixed-example-v1\",
>         \"schema\\_version\": \"t2-v1\"
>       \\}
>     \\},
>     \\{
>       \"actual\\_response\\_model\\_id\": null,
>       \"artifact\\_ids\": \\[
>         \"a9a08f9c0d2d488ca782a51298cf3d3a\"
>       \\],
>       \"attempt\\_id\": \"2bbccb7df2d44620aa5c014e8e613ced\",
>       \"candidate\\_passage\\_ids\": \\[\\],
>       \"dispatched\": true,
>       \"duration\\_seconds\": 0.0159999999741558,
>       \"errors\": \\[\\],
>       \"event\\_id\": \"22f3f6fd16574f2fa836c1f94273e173\",
>       \"finished\\_at\": \"2026-10-11T03:36:39.049254Z\",
>       \"first\\_token\\_seconds\": null,
>       \"job\\_id\": \"5f4c830275aa4855a0d52df82efe8cec\",
>       \"model\\_id\": null,
>       \"operation\": \"storage\",
>       \"original\\_processing\\_event\\_id\": null,
>       \"provider\\_request\\_id\": null,
>       \"retry\\_index\": 0,
>       \"returned\\_bytes\": null,
>       \"run\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"selected\\_passage\\_ids\": \\[\\],
>       \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"stage\": \"review\\_event\",
>       \"stage\\_id\": \"review\\_event\",
>       \"started\\_at\": \"2026-10-11T03:36:39.039894Z\",
>       \"state\": \"succeeded\",
>       \"streaming\": false,
>       \"unused\\_allowance\": null,
>       \"usage\": \\{
>         \"cache\\_read\\_tokens\": null,
>         \"cache\\_write\\_tokens\": null,
>         \"input\\_tokens\": null,
>         \"output\\_tokens\": null
>       \\},
>       \"versions\": \\{
>         \"application\": \"vs4-v1\",
>         \"chunking\": \"source-locations-v1\",
>         \"extraction\": \"vs2-v1\",
>         \"model\\_configuration\": \"controlled-response-v1\",
>         \"prompt\": \"controlled-vs3-v1\",
>         \"retrieval\": \"fixed-example-v1\",
>         \"schema\\_version\": \"t2-v1\"
>       \\}
>     \\},
>     \\{
>       \"actual\\_response\\_model\\_id\": null,
>       \"artifact\\_ids\": \\[\\],
>       \"attempt\\_id\": \"cbe13616673f43ed8ab0777fdd537cae\",
>       \"candidate\\_passage\\_ids\": \\[\\],
>       \"dispatched\": true,
>       \"duration\\_seconds\": 0.0,
>       \"errors\": \\[\\],
>       \"event\\_id\": \"38b898ce76bb4ef78387079b0fc890c2\",
>       \"finished\\_at\": \"2026-10-11T03:36:38.344863Z\",
>       \"first\\_token\\_seconds\": null,
>       \"job\\_id\": \"5f4c830275aa4855a0d52df82efe8cec\",
>       \"model\\_id\": null,
>       \"operation\": \"internal\",
>       \"original\\_processing\\_event\\_id\": null,
>       \"provider\\_request\\_id\": null,
>       \"retry\\_index\": 0,
>       \"returned\\_bytes\": null,
>       \"run\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"selected\\_passage\\_ids\": \\[
>         \"RBI-IT-2023:2023-11-07:19b\",
>         \"RBI-IT-2023:2023-11-07:2ai\",
>         \"RBI-IT-2023:2023-11-07:2b\",
>         \"9999fb6aa81340eca0424f137a044417-2\"
>       \\],
>       \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"stage\": \"context\\_selection\",
>       \"stage\\_id\": \"context\\_selection\",
>       \"started\\_at\": \"2026-10-11T03:36:38.344115Z\",
>       \"state\": \"succeeded\",
>       \"streaming\": false,
>       \"unused\\_allowance\": null,
>       \"usage\": \\{
>         \"cache\\_read\\_tokens\": null,
>         \"cache\\_write\\_tokens\": null,
>         \"input\\_tokens\": null,
>         \"output\\_tokens\": null
>       \\},
>       \"versions\": \\{
>         \"application\": \"vs4-v1\",
>         \"chunking\": \"source-locations-v1\",
>         \"extraction\": \"vs2-v1\",
>         \"model\\_configuration\": \"controlled-response-v1\",
>         \"prompt\": \"controlled-vs3-v1\",
>         \"retrieval\": \"fixed-example-v1\",
>         \"schema\\_version\": \"t2-v1\"
>       \\}
>     \\},
>     \\{
>       \"actual\\_response\\_model\\_id\": null,
>       \"artifact\\_ids\": \\[\\],
>       \"attempt\\_id\": \"e31ddc37e00643f2b33618be93df3f41\",
>       \"candidate\\_passage\\_ids\": \\[\\],
>       \"dispatched\": true,
>       \"duration\\_seconds\": 0.015000000013969839,
>       \"errors\": \\[\\],
>       \"event\\_id\": \"4c55aca2f60548088854530e9bb305e2\",
>       \"finished\\_at\": \"2026-10-11T03:36:38.437658Z\",
>       \"first\\_token\\_seconds\": null,
>       \"job\\_id\": \"5f4c830275aa4855a0d52df82efe8cec\",
>       \"model\\_id\": null,
>       \"operation\": \"storage\",
>       \"original\\_processing\\_event\\_id\": null,
>       \"provider\\_request\\_id\": null,
>       \"retry\\_index\": 0,
>       \"returned\\_bytes\": null,
>       \"run\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"selected\\_passage\\_ids\": \\[\\],
>       \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"stage\": \"persistence\",
>       \"stage\\_id\": \"persistence\",
>       \"started\\_at\": \"2026-10-11T03:36:38.427157Z\",
>       \"state\": \"succeeded\",
>       \"streaming\": false,
>       \"unused\\_allowance\": null,
>       \"usage\": \\{
>         \"cache\\_read\\_tokens\": null,
>         \"cache\\_write\\_tokens\": null,
>         \"input\\_tokens\": null,
>         \"output\\_tokens\": null
>       \\},
>       \"versions\": \\{
>         \"application\": \"vs4-v1\",
>         \"chunking\": \"source-locations-v1\",
>         \"extraction\": \"vs2-v1\",
>         \"model\\_configuration\": \"controlled-response-v1\",
>         \"prompt\": \"controlled-vs3-v1\",
>         \"retrieval\": \"fixed-example-v1\",
>         \"schema\\_version\": \"t2-v1\"
>       \\}
>     \\},
>     \\{
>       \"actual\\_response\\_model\\_id\": null,
>       \"artifact\\_ids\": \\[\\],
>       \"attempt\\_id\": \"ca6e2315dfd14c39bd9304b11012b228\",
>       \"candidate\\_passage\\_ids\": \\[
>         \"9999fb6aa81340eca0424f137a044417-1\",
>         \"9999fb6aa81340eca0424f137a044417-2\",
>         \"9999fb6aa81340eca0424f137a044417-3\",
>         \"RBI-IT-2023:2023-11-07:2a\",
>         \"RBI-IT-2023:2023-11-07:2ai\",
>         \"RBI-IT-2023:2023-11-07:2b\",
>         \"RBI-IT-2023:2023-11-07:19a\",
>         \"RBI-IT-2023:2023-11-07:19b\",
>         \"RBI-IT-2023:2023-11-07:19c\",
>         \"RBI-IT-2023:2023-11-07:29a\",
>         \"RBI-IT-2023:2023-11-07:29b\",
>         \"RBI-IT-2023:2023-11-07:29e\"
>       \\],
>       \"dispatched\": true,
>       \"duration\\_seconds\": 0.0,
>       \"errors\": \\[\\],
>       \"event\\_id\": \"8276cc35412c41ad9673217011cbd357\",
>       \"finished\\_at\": \"2026-10-11T03:36:38.323782Z\",
>       \"first\\_token\\_seconds\": null,
>       \"job\\_id\": \"5f4c830275aa4855a0d52df82efe8cec\",
>       \"model\\_id\": null,
>       \"operation\": \"retrieval\",
>       \"original\\_processing\\_event\\_id\": null,
>       \"provider\\_request\\_id\": null,
>       \"retry\\_index\": 0,
>       \"returned\\_bytes\": null,
>       \"run\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"selected\\_passage\\_ids\": \\[
>         \"RBI-IT-2023:2023-11-07:19b\",
>         \"RBI-IT-2023:2023-11-07:2ai\",
>         \"RBI-IT-2023:2023-11-07:2b\",
>         \"9999fb6aa81340eca0424f137a044417-2\"
>       \\],
>       \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"stage\": \"retrieval\",
>       \"stage\\_id\": \"retrieval\",
>       \"started\\_at\": \"2026-10-11T03:36:38.323782Z\",
>       \"state\": \"succeeded\",
>       \"streaming\": false,
>       \"unused\\_allowance\": null,
>       \"usage\": \\{
>         \"cache\\_read\\_tokens\": null,
>         \"cache\\_write\\_tokens\": null,
>         \"input\\_tokens\": null,
>         \"output\\_tokens\": null
>       \\},
>       \"versions\": \\{
>         \"application\": \"vs4-v1\",
>         \"chunking\": \"source-locations-v1\",
>         \"extraction\": \"vs2-v1\",
>         \"model\\_configuration\": \"controlled-response-v1\",
>         \"prompt\": \"controlled-vs3-v1\",
>         \"retrieval\": \"fixed-example-v1\",
>         \"schema\\_version\": \"t2-v1\"
>       \\}
>     \\},
>     \\{
>       \"actual\\_response\\_model\\_id\": null,
>       \"artifact\\_ids\": \\[\\],
>       \"attempt\\_id\": \"b7ea59e4d54c4a7783e7ccc3dcd521fc\",
>       \"candidate\\_passage\\_ids\": \\[\\],
>       \"dispatched\": true,
>       \"duration\\_seconds\": 0.01600000000325963,
>       \"errors\": \\[\\],
>       \"event\\_id\": \"cb2a8a83f7a84d2c9f8fa199e7d1128d\",
>       \"finished\\_at\": \"2026-10-11T03:36:38.380721Z\",
>       \"first\\_token\\_seconds\": null,
>       \"job\\_id\": \"5f4c830275aa4855a0d52df82efe8cec\",
>       \"model\\_id\": \"in.openai.gpt-5.6-luna\",
>       \"operation\": \"model\",
>       \"original\\_processing\\_event\\_id\": null,
>       \"provider\\_request\\_id\": null,
>       \"retry\\_index\": 0,
>       \"returned\\_bytes\": null,
>       \"run\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"selected\\_passage\\_ids\": \\[\\],
>       \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"stage\": \"model\\_call\",
>       \"stage\\_id\": \"model\\_call\",
>       \"started\\_at\": \"2026-10-11T03:36:38.368327Z\",
>       \"state\": \"succeeded\",
>       \"streaming\": false,
>       \"unused\\_allowance\": null,
>       \"usage\": \\{
>         \"cache\\_read\\_tokens\": null,
>         \"cache\\_write\\_tokens\": null,
>         \"input\\_tokens\": null,
>         \"output\\_tokens\": null
>       \\},
>       \"versions\": \\{
>         \"application\": \"vs4-v1\",
>         \"chunking\": \"source-locations-v1\",
>         \"extraction\": \"vs2-v1\",
>         \"model\\_configuration\": \"controlled-response-v1\",
>         \"prompt\": \"controlled-vs3-v1\",
>         \"retrieval\": \"fixed-example-v1\",
>         \"schema\\_version\": \"t2-v1\"
>       \\}
>     \\},
>     \\{
>       \"actual\\_response\\_model\\_id\": null,
>       \"artifact\\_ids\": \\[
>         \"9999fb6aa81340eca0424f137a044417\"
>       \\],
>       \"attempt\\_id\": \"ba84339653be4f778c0e471f8c58f7e0\",
>       \"candidate\\_passage\\_ids\": \\[\\],
>       \"dispatched\": false,
>       \"duration\\_seconds\": 0.0,
>       \"errors\": \\[\\],
>       \"event\\_id\": \"cc6041343d1d4c6fa09cee82bd59bd3c\",
>       \"finished\\_at\": \"2026-10-11T03:36:38.301767Z\",
>       \"first\\_token\\_seconds\": null,
>       \"job\\_id\": \"5f4c830275aa4855a0d52df82efe8cec\",
>       \"model\\_id\": null,
>       \"operation\": \"internal\",
>       \"original\\_processing\\_event\\_id\": \"9999fb6aa81340eca0424f137a044417\",
>       \"provider\\_request\\_id\": null,
>       \"retry\\_index\": 0,
>       \"returned\\_bytes\": null,
>       \"run\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"selected\\_passage\\_ids\": \\[\\],
>       \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"stage\": \"extraction\",
>       \"stage\\_id\": \"extraction\",
>       \"started\\_at\": \"2026-10-11T03:36:38.301767Z\",
>       \"state\": \"skipped\",
>       \"streaming\": false,
>       \"unused\\_allowance\": null,
>       \"usage\": \\{
>         \"cache\\_read\\_tokens\": null,
>         \"cache\\_write\\_tokens\": null,
>         \"input\\_tokens\": null,
>         \"output\\_tokens\": null
>       \\},
>       \"versions\": \\{
>         \"application\": \"vs4-v1\",
>         \"chunking\": \"source-locations-v1\",
>         \"extraction\": \"vs2-v1\",
>         \"model\\_configuration\": \"controlled-response-v1\",
>         \"prompt\": \"controlled-vs3-v1\",
>         \"retrieval\": \"fixed-example-v1\",
>         \"schema\\_version\": \"t2-v1\"
>       \\}
>     \\},
>     \\{
>       \"actual\\_response\\_model\\_id\": null,
>       \"artifact\\_ids\": \\[\\],
>       \"attempt\\_id\": \"5fbd0ba01ff543c08fd535c4c368acda\",
>       \"candidate\\_passage\\_ids\": \\[\\],
>       \"dispatched\": true,
>       \"duration\\_seconds\": 0.0,
>       \"errors\": \\[\\],
>       \"event\\_id\": \"f004bb6738c3495484b1367bdb4d56cf\",
>       \"finished\\_at\": \"2026-10-11T03:36:38.278280Z\",
>       \"first\\_token\\_seconds\": null,
>       \"job\\_id\": \"5f4c830275aa4855a0d52df82efe8cec\",
>       \"model\\_id\": null,
>       \"operation\": \"internal\",
>       \"original\\_processing\\_event\\_id\": null,
>       \"provider\\_request\\_id\": null,
>       \"retry\\_index\": 0,
>       \"returned\\_bytes\": null,
>       \"run\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"selected\\_passage\\_ids\": \\[\\],
>       \"snapshot\\_id\": \"13d0f2d9f7ec559f910f8c2d84b82c94\",
>       \"stage\": \"source\\_verification\",
>       \"stage\\_id\": \"source\\_verification\",
>       \"started\\_at\": \"2026-10-11T03:36:38.273033Z\",
>       \"state\": \"succeeded\",
>       \"streaming\": false,
>       \"unused\\_allowance\": null,
>       \"usage\": \\{
>         \"cache\\_read\\_tokens\": null,
>         \"cache\\_write\\_tokens\": null,
>         \"input\\_tokens\": null,
>         \"output\\_tokens\": null
>       \\},
>       \"versions\": \\{
>         \"application\": \"vs4-v1\",
>         \"chunking\": \"source-locations-v1\",
>         \"extraction\": \"vs2-v1\",
>         \"model\\_configuration\": \"controlled-response-v1\",
>         \"prompt\": \"controlled-vs3-v1\",
>         \"retrieval\": \"fixed-example-v1\",
>         \"schema\\_version\": \"t2-v1\"
>       \\}
>     \\}
>   \\]
> \\}·
## Unchecked obligations·
> \\[\\]·
## Source Version·
> \\{
>   \"document\": \\{
>     \"case\\_id\": \"41d7ddeee1f545419a5999f50dad0e74\",
>     \"document\\_version\\_id\": \"9999fb6aa81340eca0424f137a044417\",
>     \"effective\\_date\": null,
>     \"kind\": \"policy\",
>     \"publication\\_date\": null,
>     \"sha256\": \"e5b255e307bc926270d6a12c7499dce86350ab981325fd74264c344af32f9e6f\",
>     \"source\\_id\": \"03562af9a8484489ac3d8d3343c208d1\",
>     \"source\\_url\": null,
>     \"storage\\_reference\": \"9999fb6aa81340eca0424f137a044417\",
>     \"synthetic\": true,
>     \"version\": \"1\"
>   \\},
>   \"filename\": \"policy.txt\",
>   \"format\": \"txt\",
>   \"passages\": \\[
>     \\{
>       \"document\\_version\\_id\": \"9999fb6aa81340eca0424f137a044417\",
>       \"location\": \"Line 1\",
>       \"passage\\_id\": \"9999fb6aa81340eca0424f137a044417-1\",
>       \"text\": \"Synthetic demo. Fictional bank policy.\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"9999fb6aa81340eca0424f137a044417\",
>       \"location\": \"Line 2\",
>       \"passage\\_id\": \"9999fb6aa81340eca0424f137a044417-2\",
>       \"text\": \"Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"9999fb6aa81340eca0424f137a044417\",
>       \"location\": \"Line 3\",
>       \"passage\\_id\": \"9999fb6aa81340eca0424f137a044417-3\",
>       \"text\": \"Weekly timing is bank policy, not an RBI-specified interval.\"
>     \\}
>   \\],
>   \"units\": 1,
>   \"uploaded\\_at\": \"2026-10-11T03:36:38.043465\\+00:00\"
> \\}·
## Source Version·
> \\{
>   \"document\": \\{
>     \"case\\_id\": \"41d7ddeee1f545419a5999f50dad0e74\",
>     \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>     \"kind\": \"regulation\",
>     \"sha256\": \"d742aece8d2b5d74240e83e4d2ec6150a57f2076c02a9c878528ad6c42151786\",
>     \"source\\_id\": \"RBI-IT-2023\",
>     \"synthetic\": false,
>     \"version\": \"2023-11-07\"
>   \\},
>   \"effective\\_date\": \"2024-04-01\",
>   \"filename\": \"Master Direction on Information Technology Governance, Risk, Controls and Assurance Practices\",
>   \"format\": \"html\",
>   \"freshness\": \"unverified\",
>   \"passages\": \\[
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"location\": \"Clause 2\\(a\\)\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:2a\",
>       \"text\": \"These Directions shall be applicable to the following entities \\(collectively referred to as ‘regulated entities’ or ’REs’ in these directions\\):\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"location\": \"Clause 2\\(a\\)\\(i\\)\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:2ai\",
>       \"text\": \"all Banking Companies 1 , Corresponding New Banks and State Bank of India as defined under subsections \\(c\\), \\(da\\) and \\(nc\\) of section 5 of the Banking Regulation Act, 1949 \\(collectively referred to as ‘commercial banks’ hereinafter\\).\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"location\": \"Clause 2\\(b\\)\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:2b\",
>       \"text\": \"These Directions shall not be applicable to: Local Area Banks NBFC-Core Investment Companies\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"location\": \"Clause 19\\(a\\)\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:19a\",
>       \"text\": \"Access to information assets shall be allowed only where a valid business need exists. REs shall have documented standards and procedures, which are approved by the ITSC and kept up to date for administering need-based access to an information system.\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"location\": \"Clause 19\\(b\\)\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:19b\",
>       \"text\": \"Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed.\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"location\": \"Clause 19\\(c\\)\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:19c\",
>       \"text\": \"REs shall adopt multi-factor authentication for privileged users of i\\) critical information systems and ii\\) for critical activities, basis the RE’s risk assessment.\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"location\": \"Clause 29\\(a\\)\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:29a\",
>       \"text\": \"Periodicity of DR drills for critical information systems shall be at least on a half-yearly basis and for other information systems, as per RE’s risk assessment.\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"location\": \"Clause 29\\(b\\)\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:29b\",
>       \"text\": \"Any major issues observed during the DR drill shall be resolved and tested again to ensure successful conduct of drill before the next cycle.\"
>     \\},
>     \\{
>       \"document\\_version\\_id\": \"RBI-IT-2023:2023-11-07\",
>       \"location\": \"Clause 29\\(e\\)\",
>       \"passage\\_id\": \"RBI-IT-2023:2023-11-07:29e\",
>       \"text\": \"REs shall backup data and periodically restore such backed-up data to check its usability. The integrity of such backup data shall be preserved along with securing it from unauthorised access.\"
>     \\}
>   \\],
>   \"publication\\_date\": \"2023-11-07\",
>   \"source\\_url\": \"https://www.rbi.org.in/Scripts/BS\\_ViewMasDirections.aspx?id=12562\"
> \\}·
## Limitations·
> Controlled example only. No live model call occurred.
> Current regulatory status is unverified. This report does not certify bank compliance.
> A policy alone does not prove operational execution.
> Human approval measures review decisions, not assessment accuracy.
> Token usage and inference or total system cost are unknown.
> The observed job state is current. The report cutoff controls saved findings, reviews, and trace events.
"
```

# Page snapshot

```yaml
- generic [ref=e2]:
  - link "Skip to content" [ref=e3] [cursor=pointer]:
    - /url: "#main"
  - banner [ref=e4]:
    - generic [ref=e5]:
      - generic [aria-hidden] [ref=e6]: R
      - generic [ref=e7]: The Regulator
    - generic [ref=e8]:
      - generic [ref=e9]: Local development
      - button "Sign out" [ref=e10] [cursor=pointer]
  - main [ref=e11]:
    - button "← Back to cases" [ref=e12] [cursor=pointer]
    - status [ref=e13]: Case saved
    - generic [ref=e14]:
      - generic [ref=e15]:
        - generic [ref=e16]: Synthetic demo
        - heading "Fictional export bank 1791689797588" [level=1] [ref=e17]
        - paragraph [ref=e18]: Your fictional bank profile is saved.
      - generic [ref=e19]: Controlled assessment completed
    - generic [ref=e20]:
      - heading "Case details" [level=2] [ref=e21]
      - generic [ref=e22]:
        - generic [ref=e23]:
          - term [ref=e24]: Bank profile
          - definition [ref=e25]: Fictional export bank 1791689797588
        - generic [ref=e26]:
          - term [ref=e27]: Data type
          - definition [ref=e28]: Fictional data
        - generic [ref=e29]:
          - term [ref=e30]: Created
          - definition [ref=e31]: 10/11/2026, 9:06:37 AM
        - generic [ref=e32]:
          - term [ref=e33]: Case ID
          - definition [ref=e34]: 41d7ddeee1f545419a5999f50dad0e74
    - generic [ref=e35]:
      - region [ref=e36]:
        - generic [ref=e37]:
          - generic [ref=e38]:
            - paragraph [ref=e39]: SOURCE DOCUMENTS
            - heading "Documents" [level=2] [ref=e40]
            - paragraph [ref=e41]: Keep the original file and inspect its extracted text.
          - button "Refresh documents" [ref=e42] [cursor=pointer]
        - status [ref=e43]: Document saved. Earlier versions remain available.
        - generic [ref=e44]:
          - generic [ref=e45]:
            - region [ref=e46]:
              - heading "Upload a fictional document" [level=3] [ref=e47]
              - paragraph [ref=e48]: Text PDF, DOCX, TXT, or CSV. Maximum 10 MB per file and 10 saved versions per case.
              - group [ref=e50]:
                - generic [ref=e51]: Document file
                - button "Document file" [ref=e52]
                - generic [ref=e53]: Document role
                - combobox "Document role" [ref=e54]:
                  - option "Bank profile"
                  - option "Policy" [selected]
                  - option "Control"
                  - option "Evidence"
                - generic [ref=e55]: Replace source
                - combobox "Replace source" [ref=e56]:
                  - option "New source" [selected]
                  - option "policy.txt"
                - paragraph [ref=e57]: A replacement adds a version. It keeps the earlier version.
                - generic [ref=e58]:
                  - checkbox "I confirm this document contains fictional data only." [ref=e59]
                  - generic [ref=e60]: I confirm this document contains fictional data only.
                - button "Upload fictional document" [disabled] [ref=e61]
            - region [ref=e62]:
              - heading "Saved versions 1" [level=3] [ref=e63]
              - button "Inspect policy.txt version 1" [pressed] [ref=e64] [cursor=pointer]:
                - strong [ref=e65]: policy.txt
                - generic [ref=e66]: policy · Version 1 · TXT
          - region [ref=e67]:
            - heading "Source evidence" [level=3] [ref=e68]
            - generic [ref=e69]:
              - generic [ref=e70]:
                - heading "policy.txt" [level=3] [ref=e71]
                - paragraph [ref=e72]: Version 1 · policy · TXT
              - button "Download original" [ref=e73] [cursor=pointer]
            - paragraph [ref=e74]: Extracted text can omit images and visual table structure. Use the original file to check them.
            - paragraph [ref=e75]: "Version ID: 9999fb6aa81340eca0424f137a044417"
            - group [ref=e76]:
              - generic "Content hash (SHA-256)" [ref=e77]
            - generic [ref=e78]:
              - article [ref=e79]:
                - heading "Line 1" [level=4] [ref=e80]
                - generic [ref=e81]: Synthetic demo. Fictional bank policy.
              - article [ref=e82]:
                - heading "Line 2" [level=4] [ref=e83]
                - generic [ref=e84]: Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.
              - article [ref=e85]:
                - heading "Line 3" [level=4] [ref=e86]
                - generic [ref=e87]: Weekly timing is bank policy, not an RBI-specified interval.
      - region [ref=e88]:
        - generic [ref=e89]:
          - generic [ref=e90]:
            - paragraph [ref=e91]: CONTROLLED EXAMPLE
            - heading "Assessment" [level=2] [ref=e92]
            - paragraph [ref=e93]: Review one fictional policy against a selected historical or simulated rule.
          - button "Refresh assessment" [ref=e94] [cursor=pointer]
        - generic [ref=e95]:
          - paragraph [ref=e96]: Use the supplied fictional policy. Other documents cannot run this controlled example.
          - paragraph [ref=e97]:
            - link "Download the fictional policy" [ref=e98] [cursor=pointer]:
              - /url: data:text/plain;charset=utf-8,…
            - text: ", then upload it as a policy document."
          - generic [ref=e99]: Policy version
          - combobox "Policy version" [ref=e100]:
            - option "Upload a fictional policy first"
            - option "policy.txt · Version 1" [selected]
          - generic [ref=e101]: Regulatory source
          - combobox "Regulatory source" [ref=e102]:
            - option "RBI clause 19(b) · historical 2023 version" [selected]
            - option "Simulated access rule · v1"
          - paragraph [ref=e103]: "Historical date: 8 April 2024. Current regulatory status is unverified. No live model call is made."
          - button "Run controlled assessment" [ref=e104] [cursor=pointer]
          - generic [ref=e105]: Saved assessments
          - combobox "Saved assessments" [ref=e106]:
            - option "Select a saved assessment"
            - option "10/11/2026, 9:06:38 AM · 5f4c8302" [selected]
        - region "Regulatory changes" [ref=e107]:
          - heading "Regulatory changes" [level=2] [ref=e108]
          - generic [ref=e109]: Synthetic regulatory simulation
          - paragraph [ref=e110]: Compare specified fictional versions. Earlier assessments and human reviews stay unchanged.
          - paragraph [ref=e111]: These examples do not establish current regulatory coverage or live model quality.
          - paragraph [ref=e112]: Run or open a completed simulated v1 assessment to select the earlier version.
        - region "Assessment result" [ref=e113]:
          - generic [ref=e114]:
            - generic [ref=e115]: Controlled simulation
            - heading "Needs review" [level=3] [ref=e116]
            - paragraph [ref=e117]: This is a fixed example. It does not establish compliance or current regulatory coverage.
          - generic [ref=e118]:
            - article [ref=e119]:
              - heading "Requirement and applicability" [level=3] [ref=e120]
              - paragraph [ref=e121]: Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed.
              - paragraph [ref=e122]: Unverified for this fictional bank profile.
              - heading "Conditions" [level=4] [ref=e123]
              - list [ref=e124]:
                - listitem [ref=e125]: Personnel with elevated system access entitlements.
                - listitem [ref=e126]: Applicability to the listed regulated entities must be established.
              - heading "Exceptions" [level=4] [ref=e127]
              - list [ref=e128]:
                - listitem [ref=e129]: Local Area Banks
                - listitem [ref=e130]: NBFC-Core Investment Companies
              - heading "Policy control" [level=4] [ref=e131]
              - paragraph [ref=e132]: Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.
              - paragraph [ref=e133]: Weekly timing is bank policy. RBI does not specify that interval in this clause.
              - generic [ref=e134]:
                - button "Inspect Clause 19(b)" [ref=e135] [cursor=pointer]
                - button "Inspect Clause 2(a)(i)" [ref=e136] [cursor=pointer]
                - button "Inspect Clause 2(b)" [ref=e137] [cursor=pointer]
            - article [ref=e138]:
              - heading "Original finding" [level=3] [ref=e139]
              - paragraph [ref=e140]: Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.
              - heading "Proposed recommendation" [level=4] [ref=e141]
              - paragraph [ref=e142]: Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.
              - button "Inspect policy Line 2" [ref=e144] [cursor=pointer]
              - group "Human review" [ref=e146]:
                - generic [ref=e148]:
                  - generic [ref=e149]:
                    - radio "Approved" [checked] [ref=e150]
                    - text: Approved
                  - generic [ref=e151]:
                    - radio "Edited" [ref=e152]
                    - text: Edited
                  - generic [ref=e153]:
                    - radio "Rejected" [ref=e154]
                    - text: Rejected
                  - generic [ref=e155]:
                    - radio "Request more evidence" [ref=e156]
                    - text: Request more evidence
                - generic [ref=e157]: Review reason
                - textbox "Review reason" [ref=e158]
                - button "Save review" [ref=e159] [cursor=pointer]
          - generic [ref=e160]:
            - heading "Saved review outcomes" [level=3] [ref=e161]
            - paragraph [ref=e162]: "Approved: 1 · Edited: 0 · Rejected: 0 · Pending: 0"
            - paragraph [ref=e163]: "Eligible: 1 · Reviewed: 1"
            - paragraph [ref=e164]: "Approval without edits: 100%"
            - paragraph [ref=e165]: "Edit rate: 0% · Rejection rate: 0%"
            - paragraph [ref=e166]: "Adoption with or without edits: 100%"
            - paragraph [ref=e167]: "Review coverage: 100%"
            - paragraph [ref=e168]: These figures measure human review decisions. They do not measure correctness. Latest final decisions count at the shown cutoff.
            - paragraph [ref=e169]: "Cutoff: 2026-10-11T03:36:39.074540+00:00 · Definition: d24-v1"
            - article [ref=e170]:
              - heading "Approved · Revision 1" [level=4] [ref=e171]
              - paragraph [ref=e172]: Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.
              - paragraph [ref=e173]: Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.
          - region "Export assessment" [ref=e174]:
            - heading "Export assessment" [level=3] [ref=e175]
            - paragraph [ref=e176]: Download the saved versions, source passages, findings, and human reviews at the displayed cutoff.
            - paragraph [ref=e177]: Controlled simulation. Current regulatory status is unverified. Usage and cost remain unknown.
            - generic [ref=e178]:
              - button "Download JSON" [ref=e179] [cursor=pointer]
              - button "Download Markdown" [ref=e180] [cursor=pointer]
          - group [ref=e181]:
            - generic "Saved run record" [ref=e182] [cursor=pointer]
  - contentinfo [ref=e183]: Fictional case workspace · Development release
```

# Test source

```ts
  1  | import { expect, test, type Page, type Download } from '@playwright/test';
  2  | import { readFileSync } from 'node:fs';
  3  | const evidenceDir = process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-11-slice-05-release';
  4  |
  5  | async function assessment(page: Page) {
  6  |   await page.goto('/');
  7  |   await page.getByRole('button', {name: 'Continue with local identity'}).click();
  8  |   await page.getByLabel('Fictional bank name').fill(`Fictional export bank ${Date.now()}`);
  9  |   await page.getByLabel('I confirm this case contains fictional data only.', {exact:true}).check();
  10 |   await page.getByRole('button', {name: 'Save fictional case'}).click();
  11 |   await page.getByLabel('Document file', {exact:true}).setInputFiles({name:'policy.txt',mimeType:'text/plain',buffer:readFileSync('../../data/fixtures/slice-02-policy.txt')});
  12 |   await page.getByLabel('I confirm this document contains fictional data only.', {exact:true}).check();
  13 |   await page.getByRole('button', {name:'Upload fictional document',exact:true}).click();
  14 |   await page.getByRole('button', {name:'Run controlled assessment',exact:true}).click();
  15 |   const result = page.getByRole('region',{name:'Assessment result',exact:true});
  16 |   await expect(result).toContainText('Needs review');
  17 |   return result;
  18 | }
  19 |
  20 | async function text(download: Download) {
  21 |   expect(await download.failure()).toBeNull();
  22 |   return readFileSync((await download.path())!, 'utf8');
  23 | }
  24 |
  25 | test('VS5-BT01 JSON and Markdown downloads preserve saved review and exact sources',async ({page}) => {
  26 |   const result = await assessment(page);
  27 |   await page.getByLabel('Approved',{exact:true}).check();
  28 |   await page.getByRole('button',{name:'Save review',exact:true}).click();
  29 |   await expect(result).toContainText('Approved · Revision 1');
  30 |   const expected = await result.locator('.identifier').first().innerText();
  31 |   const [json] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download JSON',exact:true}).click()]);
  32 |   const report = JSON.parse(await text(json));
  33 |   expect(report.summary.approved).toBe(1);
  34 |   expect(report.summary.approval_rate).toBe(1);
  35 |   expect(report.snapshot.snapshot_id).toBeTruthy();
  36 |   expect(report.sources).toHaveLength(2);
  37 |   expect(report.data_mode).toBe('controlled_simulation');
  38 |   expect(report.label).toContain('Simulated');
  39 |   expect(report.cost_usd).toBeNull();
  40 |   expect(report.findings[0].status).toBe('needs_review');
  41 |   const [markdown] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download Markdown',exact:true}).click()]);
  42 |   const contents = await text(markdown);
  43 |   expect(contents).toContain(report.snapshot.snapshot_id);
  44 |   expect(contents).toContain('approved: 1');
> 45 |   expect(contents).toContain('Clause 19(b)');
     |                    ^ Error: expect(received).toContain(expected) // indexOf
  46 |   expect(contents).toContain('cost: Unknown');
  47 |   await expect(result).toContainText(expected);
  48 |   await json.saveAs(`${evidenceDir}/export-example.json`);
  49 |   await markdown.saveAs(`${evidenceDir}/export-example.md`);
  50 |   await page.screenshot({path:`${evidenceDir}/release-desktop.png`,fullPage:true});
  51 | });
  52 |
  53 | test('VS5-BT02 export failure preserves saved review and retry succeeds',async ({page}) => {
  54 |   const result = await assessment(page);
  55 |   await page.getByLabel('Approved',{exact:true}).check();
  56 |   await page.getByRole('button',{name:'Save review',exact:true}).click();
  57 |   await expect(result).toContainText('Approved · Revision 1');
  58 |   const job = new URL(page.url()).searchParams.get('assessment');
  59 |   await page.route('**/assessments/*/export*',route=>route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({message:'Export unavailable.',next_action:'Retry the export.'})}),{times:1});
  60 |   await page.getByRole('button',{name:'Download JSON',exact:true}).click();
  61 |   await expect(page.getByRole('alert')).toContainText('Export unavailable');
  62 |   await expect(result).toContainText('Approved · Revision 1');
  63 |   expect(new URL(page.url()).searchParams.get('assessment')).toBe(job);
  64 |   const [download] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download JSON',exact:true}).click()]);
  65 |   expect(JSON.parse(await text(download)).summary.approved).toBe(1);
  66 | });
  67 |
  68 | test('VS5-BT03 mobile keyboard download keeps labels and does not overflow',async ({page}) => {
  69 |   await page.setViewportSize({width:390,height:844});
  70 |   const result = await assessment(page);
  71 |   const download = page.getByRole('button',{name:'Download JSON',exact:true});
  72 |   await download.focus();
  73 |   const [file] = await Promise.all([page.waitForEvent('download'),page.keyboard.press('Enter')]);
  74 |   expect(JSON.parse(await text(file)).label).toContain('Simulated');
  75 |   expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
  76 |   await expect(result).toContainText('Not measured');
  77 |   await page.screenshot({path:`${evidenceDir}/release-mobile.png`,fullPage:true});
  78 | });
  79 |
```
