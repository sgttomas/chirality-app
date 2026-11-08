# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-09/DEL-09-02/Work/j1_picker_diagnostic.py` | `app/examination/native_support/j1_picker_diagnostic.py` | `ab48a7eb395d731e65c6edf0d839b83f0fe1581595b78b951c08558cb127c8c6` | no |
| `execution/PKG-09/DEL-09-02/Work/j1_stage_a_phase.py` | `app/examination/native_support/j1_stage_a_phase.py` | `f510d9be6a4e2e8d8eb77f25642e1f16a33f13c8d909898ff7f71ff6f6a3ccdc` | no |
| `execution/PKG-09/DEL-09-02/Work/native_attended_admission.py` | `app/examination/native_support/native_attended_admission.py` | `ecc453a3687c8408f64f459baa4a7c13ac39adb0f2000cd74fff08226d2f5dd7` | no |
| `execution/PKG-09/DEL-09-02/Work/native_attended_bridge.py` | `app/examination/native_support/native_attended_bridge.py` | `5cd8b14a6c9ea9e7a92f537be8154087899df23d47567e58604b69ad99d04607` | no |
| `execution/PKG-09/DEL-09-02/Work/native_attended_disposition.py` | `app/examination/native_support/native_attended_disposition.py` | `65567c204b0ff78a46abeff0b2ff214e591a7d1f33d681ea4a8ee14c2ced38fc` | no |
| `execution/PKG-09/DEL-09-02/Work/native_attended_entry.py` | `app/examination/native_support/native_attended_entry.py` | `b4922fe4ade28c068a156ff1c98166f7a7f352bd81fc306cb241ee10d360a076` | no |
| `execution/PKG-09/DEL-09-02/Work/native_attended_manager.js` | `app/examination/native_support/native_attended_manager.js` | `d4b385ded3ac64a9990613cd12fbaaeb2e7b011f185e9c5116cca48b6ef538d9` | no |
| `execution/PKG-09/DEL-09-02/Work/native_attended_owner.py` | `app/examination/native_support/native_attended_owner.py` | `b24fd4cdfd9ef7c0e640aabce441f5ce7e4ade3b8999c0c16b807d3c2863d13c` | no |
| `execution/PKG-09/DEL-09-02/Work/native_attended_ports.py` | `app/examination/native_support/native_attended_ports.py` | `f978281e70f49f0398ec85dd0c3f00f625e413c7b271f9fe9b741cddf279f157` | no |
| `execution/PKG-09/DEL-09-02/Work/native_attended_readback.py` | `app/examination/native_support/native_attended_readback.py` | `7e0719e35dd392b2dd073e56735c02068889725ef3d7da59f1f6e9bb4a3f497e` | no |
| `execution/PKG-09/DEL-09-02/Work/native_attended_retained_shell.py` | `app/examination/native_support/native_attended_retained_shell.py` | `d1b05dbf44d92636134fb5944161a4c449c2a09d97448f95dbdedd9fcfab6e31` | no |
| `execution/PKG-09/DEL-09-02/Work/native_attended_sequence.py` | `app/examination/native_support/native_attended_sequence.py` | `261affc1a5b2fbd044d3ed78b1fc7406c2bcb229ec2fa556d7a385f4885db103` | no |
| `execution/PKG-09/DEL-09-02/Work/native_ax_comparison.py` | `app/examination/native_support/native_ax_comparison.py` | `f5ecbfae4a18495cdea19a3e6f0fa609e414be1a9775624b76f206c61a478b1d` | no |
| `execution/PKG-09/DEL-09-02/Work/native_ax_comparison_helper.py` | `app/examination/native_support/native_ax_comparison_helper.py` | `eb10703900209d7d4468989a5179b709716eaa42373a37c12c9e461bfdbcda90` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_ax.py` | `app/examination/native_support/native_b_ax.py` | `4a5a26d43063f271188a90c290e3bae56cc7794014149ca5ae7504b005737cef` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_ax_route.py` | `app/examination/native_support/native_b_ax_route.py` | `fe9362da0dd42cf757a1c65dfc24d5ded6b81494c0b6342481768ac209d06ede` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_diagnostic.py` | `app/examination/native_support/native_b_diagnostic.py` | `fd37834b301f138963cdfe76f8bf3a146aea373b99ab2c994546ff73c939af19` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_release.py` | `app/examination/native_support/native_b_release.py` | `9db06d8066ba86e78d58ea9b0719e6c7c445fdb46feb3e3f03b3a89ed51b5ec5` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_retained.py` | `app/examination/native_support/native_b_retained.py` | `82d08f4c7e5f2ec74ea8533877b76f032142f1e18e1fe757a092d2c8032685de` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_retained_v2.py` | `app/examination/native_support/native_b_retained_v2.py` | `0b6373d9281e01831902fe43213ecb7c51eaa44e769737413cafb6d666a7a42b` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_retained_v3.py` | `app/examination/native_support/native_b_retained_v3.py` | `ebafb3a456091c662762b1333293e2f17b198afb2fc19bb81441b5410955a598` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_retained_v4.py` | `app/examination/native_support/native_b_retained_v4.py` | `db3d690925821e07f1d8d55a9ad9bf477b14179f29719bd202e24acb20aa789c` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_retained_v5.py` | `app/examination/native_support/native_b_retained_v5.py` | `586d5f55906333eb686a2d6bfb7fdb1a85ab7bc9569f80961454b03d2dc209c3` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_retained_v6.py` | `app/examination/native_support/native_b_retained_v6.py` | `25c944b13eaab77e7394e5a7c300f85863bf13dc93431387edd8b1b57764269f` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_retained_v7.py` | `app/examination/native_support/native_b_retained_v7.py` | `581079c11b0ebe13888e041a2a4f87d99208ccce55a4855f9bda887598612c7a` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_retained_v8.py` | `app/examination/native_support/native_b_retained_v8.py` | `58e329e9d4c13994816a1b7a678af8a1a41d600d4bae4e9f6d4ed32d19eafa78` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_screen_route.py` | `app/examination/native_support/native_b_screen_route.py` | `6f23c2e58d20bffec1a38c9e638827304be36f08f6917211636aed229de9c363` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_slot_entry.py` | `app/examination/native_support/native_b_slot_entry.py` | `f13bee8fc965951b3cce2a6b285e47b7674dd9c2a1883aa4ae47403c4de46f08` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_typed_ax.py` | `app/examination/native_support/native_b_typed_ax.py` | `95847b744db0e88c7ceaa618fa9e87713e08badd257f91c30974c5f8b1c69b80` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_window.py` | `app/examination/native_support/native_b_window.py` | `75f59b04796bed3532c658ed858529a8d88dbb0c5b3c3c900dbe80bf6a0ca0f4` | no |
| `execution/PKG-09/DEL-09-02/Work/native_b_window_helper.py` | `app/examination/native_support/native_b_window_helper.py` | `d412eab2260592939e8ee018527c6bc5a76d029b8487200037004051c543b910` | no |
| `execution/PKG-09/DEL-09-02/Work/native_setup_continuation.py` | `app/examination/native_support/native_setup_continuation.py` | `371f46551f7f4cb21683235bcfe7bfa84cc8b9082db07fb1e2806b3103790e85` | no |
| `execution/PKG-09/DEL-09-02/Work/native_sheet_cancel.py` | `app/examination/native_support/native_sheet_cancel.py` | `9f34fd0af4d1c65d50b3735c02461c4bed19c53115f1e44944563cf92cd19ba7` | no |
| `execution/PKG-09/DEL-09-02/Work/native_successor_relaunch.py` | `app/examination/native_support/native_successor_relaunch.py` | `64ed5bc0993fd64b831fcfa95651d74592497ea625cb3fa73ca27844ee630ed4` | no |
| `execution/PKG-09/DEL-09-02/Work/native_successor_setup.py` | `app/examination/native_support/native_successor_setup.py` | `07895706c6a1c336b51ac0c9377f7b2fe086d6e3b36904ac794691288fce841f` | no |
| `execution/PKG-09/DEL-09-02/Work/native_visual_session.py` | `app/examination/native_support/native_visual_session.py` | `cf58b8b219167c5d7551d0f14e43e5736b8a386a1befd1185c8b5a520d563973` | no |
| `execution/PKG-09/DEL-09-02/Work/prototype/check_sq.py` | `app/contract_inputs/PKG-09/DEL-09-02/Work/prototype/check_sq.py` | `6067c5ec2ef1215c7650bfb51f6fc6aaff79c41bb4b1c3940a5acefb397915ef` | yes |
| `execution/PKG-09/DEL-09-02/Work/signed_witness_collect.sh` | `app/examination/native_support/signed_witness_collect.sh` | `632648791e47fa7964d4e0b76d295fbaa675b4f9010bd99582311f282faf9ac7` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_admission.py` | `app/examination/native_support/test_native_attended_admission.py` | `a871930a5249c2064cbe3ae41226a0523d4af268f7cd2e3b53319f91ed8f586d` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_autonomous.py` | `app/examination/native_support/test_native_attended_autonomous.py` | `90d318d33382fa2ddb5c7c545195c52db39e379e9777f66509a5f4b6814a898a` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_diagnostic.py` | `app/examination/native_support/test_native_attended_diagnostic.py` | `6c87b3107584df556e960d6769d7b89bf9ffcb486022d3dd5397966d341054e9` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_disposition.py` | `app/examination/native_support/test_native_attended_disposition.py` | `eac283ddc686d17cff3cd7c3836f1174d23222a4cde33e2b4a950e9c48a90e4e` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_early_quit.py` | `app/examination/native_support/test_native_attended_early_quit.py` | `da9dd0295178acb3b4c70278f210da7b93ac22dfc6bb9bbafe1f5fad1b437711` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_entry.py` | `app/examination/native_support/test_native_attended_entry.py` | `f4f5a1a28c6b995ab934d79677242da87a244c0bf71063be3ead132ae3d9dac7` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_foreground.py` | `app/examination/native_support/test_native_attended_foreground.py` | `ada174a1771eaba7bc2e47e05bd117f79d3633d518614533d77e670441b1cd7d` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_helper_contract.py` | `app/examination/native_support/test_native_attended_helper_contract.py` | `5ea1c812980c9e7623b38ac9320027559140de9b4c34fe550d02073c05616f83` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_j1_phase.py` | `app/examination/native_support/test_native_attended_j1_phase.py` | `a9420fa679756cda260f13d9be2acfbeef7f0a66a6962ab5b3ff5bb1d130998e` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_launch_overrides.py` | `app/examination/native_support/test_native_attended_launch_overrides.py` | `2ecbfce17e8f2cb4ef9410a81b6dcc1668fd55c834d3aea1fe44a42afe7b1d16` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_manager.cjs` | `app/examination/native_support/test_native_attended_manager.cjs` | `bf42020de175525c3decdf15cb3d5e3d1dadf7a8512919547644f2c66e45991e` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_owner.py` | `app/examination/native_support/test_native_attended_owner.py` | `f69745ffe0673a8045aa6f7dfe1dd1efb9275c26e1998c83c36fd766d94bc00f` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_picker_diagnostic.py` | `app/examination/native_support/test_native_attended_picker_diagnostic.py` | `3f106a3dd1ac94d2a072412c4f4547dda57b1ef3a82f055099138c2c18f66c99` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_ports.py` | `app/examination/native_support/test_native_attended_ports.py` | `cb31bbf2ef3c5eb35dbbff0e0fa1786b8a393fecc3ceefaa8be9f8e7cd5c333d` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_readback.py` | `app/examination/native_support/test_native_attended_readback.py` | `8f24c650b902c67d6e9d3a8637b10e13e87da828cf0e945d706aac7fb5eb60e0` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_retained_shell.py` | `app/examination/native_support/test_native_attended_retained_shell.py` | `2efa69d9a87a295ccaca170105961b3ba3e6ee7a73a6e4f8eb0079a33f4cc076` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_attended_sequence.py` | `app/examination/native_support/test_native_attended_sequence.py` | `db293f6f4e4335e0195bee6739ec43438aedc365fcf42d29ada6851fcae711ff` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_ax.py` | `app/examination/native_support/test_native_b_ax.py` | `0d9aa2607937228609224ebfe79006b8d412b15ae7ee18a9b9dccc185b4598f5` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_ax_route.py` | `app/examination/native_support/test_native_b_ax_route.py` | `a1edb082b10b6b5c16569f847dc24056837f4536a7aedf037c27f1d707606849` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_diagnostic.py` | `app/examination/native_support/test_native_b_diagnostic.py` | `2060c5ffde276d77451113cae4500832aa42cf0b9cf15d45580d4a5afe22e957` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_guard.py` | `app/examination/native_support/test_native_b_guard.py` | `ae93a78bea0309d4d3e2d54d8dd669a0a773f503e382baa7de48ce29d796e505` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_initial_stability.py` | `app/examination/native_support/test_native_b_initial_stability.py` | `9fe4d3a528da58e859b391da51c66fa4037ecc2003532f7ee41fb38bcadff394` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_modal.py` | `app/examination/native_support/test_native_b_modal.py` | `ac7ce84625f46e662849f7350ba6d66a812084c38342707990d335dc5c445782` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_profile.py` | `app/examination/native_support/test_native_b_profile.py` | `284a06159726f25ed9645454deea1799af40f51e3658758a562e4f3518cb694f` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_release.py` | `app/examination/native_support/test_native_b_release.py` | `5f014072167e3e012eb40e1a642f8526164c0724bc0d4feff59b462299ec3d97` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_retained.py` | `app/examination/native_support/test_native_b_retained.py` | `f941e5d879263f409c0aab1f556a1e5951839a620bd1333a951718af389c26be` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_retained_v2.py` | `app/examination/native_support/test_native_b_retained_v2.py` | `d9903c346e386de0398f641549e1128b86223c6ca1d7231eca5d7d151778501e` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_retained_v3.py` | `app/examination/native_support/test_native_b_retained_v3.py` | `9975dea0db5e0bbfb399a8addbd9d278c77779dad1198158fdb4df0e6acff431` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_retained_v4.py` | `app/examination/native_support/test_native_b_retained_v4.py` | `4f2ed914ab21665910798429dfd64666e699386ba192ba988e3b8ca0336450c7` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_retained_v5.py` | `app/examination/native_support/test_native_b_retained_v5.py` | `0b8a3c8918e25d2871c76b9029aa6e2cb06c9706de1f375c82f4746da2cec65b` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_retained_v6.py` | `app/examination/native_support/test_native_b_retained_v6.py` | `465bc412f17ddfc074e82a4986329e0179b5e0bd80dad7e523e9909e4e9662f0` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_retained_v7.py` | `app/examination/native_support/test_native_b_retained_v7.py` | `19e83535f9c02f1887dcdb05a9cdcb433061729e2473611058539d2761fa7302` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_retained_v8.py` | `app/examination/native_support/test_native_b_retained_v8.py` | `69203c5d9e29edffb7a70bab9d302b5bc5107c793c355c43d245250bbe94b336` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_screen_integration.py` | `app/examination/native_support/test_native_b_screen_integration.py` | `3f7fe241bdec1b104451b8af2c3210b265cc382d90def8da4f975632ab58fcb5` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_screen_route.py` | `app/examination/native_support/test_native_b_screen_route.py` | `6edbdbd8394c8c5bf00dcc2ea20526121a4334daaed54fc65fa032043fcd9bc6` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_slot_entry.py` | `app/examination/native_support/test_native_b_slot_entry.py` | `4af32247effa0f5020b2472678e93a1bb95828bd4d0ecd8587b3e7e1c3eb2d28` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_typed_ax.py` | `app/examination/native_support/test_native_b_typed_ax.py` | `6e14663f30c14351e9478c51d05b1aace110eb3baf6be1b8ad365570a0b0ce51` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_window.py` | `app/examination/native_support/test_native_b_window.py` | `0bcdd6208e1e7f6fca6741bc329afb40c13430f25a76de81c2badab4ec9ace89` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_b_window_helper.py` | `app/examination/native_support/test_native_b_window_helper.py` | `80ab040414c441c89e3349e163c965712a8301810e99e9e68ff34a9eea2c0a86` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_relaunch_policy.py` | `app/examination/native_support/test_native_relaunch_policy.py` | `a709d6815b732082afd25ed147e78da8abb47e45dc7b7fa3d3730ff91a31279b` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_setup_continuation.py` | `app/examination/native_support/test_native_setup_continuation.py` | `3c513a3857f94b896ac361c85dcc93be93eec7e5647771054586453e27444ab5` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_sheet_cancel.py` | `app/examination/native_support/test_native_sheet_cancel.py` | `ce36d0da3300be04256d06472ef8c466385eea6068c0d6cd0e8f101e934f9963` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_successor_relaunch.py` | `app/examination/native_support/test_native_successor_relaunch.py` | `f5c7be4fab41842976467b54238e3e76a9c1b77643feb60707e5dd986f4edcc4` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_successor_setup.py` | `app/examination/native_support/test_native_successor_setup.py` | `7db1e984bfc027fc293b4f7c1794f83220feebfc053d2d2428c58c25f3bbee38` | no |
| `execution/PKG-09/DEL-09-02/Work/test_native_visual_session.py` | `app/examination/native_support/test_native_visual_session.py` | `503950ec8eb0ca58b2280d7039ffcfd1773ddf9d9748eeecbc810c6bf2d5d823` | no |
| `execution/PKG-09/DEL-09-02/Work/test_signed_witness_collect.py` | `app/examination/native_support/test_signed_witness_collect.py` | `642901d3a5fcf09b2ee969ec76098ad5b3d59f1b7f02852e7f75d9d618b78ee4` | no |
| `execution/PKG-09/DEL-09-02/Work/typed_ax/build.py` | `app/examination/native_support/typed_ax/build.py` | `414a4abdc03c02f80d0b9c5bf8ffcd53d640766a6b8d1b7d44987f1676e4a5d4` | no |
| `execution/PKG-09/DEL-09-02/Work/typed_ax/fixture.c` | `app/examination/native_support/typed_ax/fixture.c` | `4c390a363d1f2c219fbdcb1e122ac2cfdc4f5bb7240e1a0b79e195c08684a456` | no |
| `execution/PKG-09/DEL-09-02/Work/typed_ax/fixture_api.h` | `app/examination/native_support/typed_ax/fixture_api.h` | `35b0e9aaa523f38ebb5b62738502b5e3366588514420bb898f76acffa9e71ffa` | no |
| `execution/PKG-09/DEL-09-02/Work/typed_ax/reader.c` | `app/examination/native_support/typed_ax/reader.c` | `df46ae32f1cd8aa361d66cf16512d0b07a07475958ebf5d56b2abe6851cd981d` | no |
| `execution/PKG-09/DEL-09-02/Work/typed_ax/reader.h` | `app/examination/native_support/typed_ax/reader.h` | `a1f3b6108d1bc178956790236d6edef67fb61501f36bc01d42a8f7884c4ea918` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
