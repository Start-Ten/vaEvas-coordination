# H Failure Taxonomy: `/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/condition-G-targeted-materialized-spectre-aligned-kimi-evas-2026-04-28`

## Counts

| family | count |
|---|---:|
| `counter_cadence/off-by-one` | 1 |
| `sampled_latch/reset_priority` | 1 |
| `quantizer/code_coverage` | 2 |
| `onehot/thermometer/no-overlap` | 3 |
| `frame/sequence_alignment` | 1 |
| `PFD/PLL timing_window` | 6 |
| `multi-module interface sanity` | 1 |
| `compile/preflight` | 2 |
| `unsupported/behavior_other` | 10 |
| `pass` | 65 |

## Failed Tasks

| task | H family | reason | status | notes |
|---|---|---|---|---|
| `adc_dac_ideal_4b_smoke` | `quantizer/code_coverage` | `code_coverage_or_unique_codes` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:8,inserted:1,signals:8
generated_include=adc_ideal_4b.va
generated_include=dac_ideal_4b.va
spectre_strict:preflight_pass
returncode=0
streaming_checker |
| `adpll_ratio_hop_smoke` | `unsupported/behavior_other` | `no_supported_signature` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:6
generated_include=adpll_ratio_hop_ref.va
spectre_strict:preflight_pass
returncode=0
pre_window_not_enough_edges num=0 den=80 |
| `adpll_timer` | `PFD/PLL timing_window` | `pulse_phase_lock_window` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:4
spectre_strict:preflight_pass
returncode=0
streaming_checker:late_edge_ratio=1.040 lock_time=6.047e-08 vctrl_range_ok=False |
| `adpll_timer_smoke` | `PFD/PLL timing_window` | `pulse_phase_lock_window` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:4,inserted:1,signals:4
generated_include=adpll_timer_ref.va
spectre_strict:preflight_pass
returncode=0
streaming_checker:late_edge_ratio=0.520 lock_tim |
| `bbpd` | `onehot/thermometer/no-overlap` | `onehot_overlap_or_pointer` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:5
spectre_strict:preflight_pass
returncode=0
data_edges=150 up_edges=0 down_edges=0 overlap_frac=0.0000 |
| `bbpd_data_edge_alignment_smoke` | `unsupported/behavior_other` | `no_supported_signature` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:5
generated_include=bbpd_data_edge_alignment_ref.va
spectre_strict:preflight_pass
returncode=0
lag_window_updn=5/1 |
| `bg_cal` | `unsupported/behavior_other` | `no_supported_signature` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:9
spectre_strict:interface_parameter_missing=bg_cal:navg instance=XDUT passed=navg declared=N,tdel,tfall,trise,vhi,vlo,vth
spectre |
| `cdac_cal` | `unsupported/behavior_other` | `no_supported_signature` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:5
spectre_strict:preflight_pass
returncode=0
no vdac activity in ['VDAC_P', 'VDAC_N', 'vdac_p', 'vdac_n'] |
| `clk_divider` | `PFD/PLL timing_window` | `pulse_phase_lock_window` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:12
spectre_strict:preflight_pass
returncode=0
not enough clock edges |
| `comparator_hysteresis_smoke` | `unsupported/behavior_other` | `no_supported_signature` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:4,inserted:1,signals:4
generated_include=cmp_hysteresis.va
spectre_strict:preflight_pass
returncode=0
window_fracs pre=1.000 mid=0.395 post=0.000 |
| `cppll_freq_step_reacquire_smoke` | `PFD/PLL timing_window` | `pulse_phase_lock_window` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:5
generated_include=cppll_timer_ref.va
spectre_strict:preflight_pass
returncode=0
streaming_checker:pre_lock_edges=0 disturb_lock_ |
| `cppll_timer` | `multi-module interface sanity` | `missing_csv_or_missing_generated_artifact` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:5
spectre_strict:interface_parameter_missing=cppll_timer_ref:div_ratio,f_center,f_max,f_min,ki,kp,kvco_hz_per_v,lock_count_target, |
| `cppll_tracking_smoke` | `PFD/PLL timing_window` | `pulse_phase_lock_window` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:4,inserted:1,signals:5
generated_include=cppll_timer_ref.va
spectre_strict:preflight_pass
returncode=0
freq_ratio=0.7259 fb_jitter_frac=0.0001 lock_tim |
| `cross_hysteresis_window_smoke` | `unsupported/behavior_other` | `no_supported_signature` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:2
generated_include=cross_hysteresis_window_ref.va
spectre_strict:preflight_pass
returncode=0
low1=0.000 high=0.237 low2=0.108 spa |
| `dwa_ptr_gen_no_overlap_smoke` | `onehot/thermometer/no-overlap` | `onehot_overlap_or_pointer` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:6,inserted:1,signals:35
generated_include=dwa_ptr_gen_no_overlap.va
spectre_strict:preflight_pass
returncode=0
streaming_checker:sampled_cycles=17 bad_ |
| `dwa_ptr_gen_smoke` | `compile/preflight` | `compile_or_spectre_strict` | `FAIL_TB_COMPILE` | contract_save_pruned=removed:10,inserted:1,signals:34
generated_include=v2b_4b.va
generated_include=dwa_ptr_gen.va
spectre_strict:preflight_pass
returncode=1
evas_log_diagnostic=ER |
| `multimod_divider` | `counter_cadence/off-by-one` | `base_pre_post_count` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:7
spectre_strict:preflight_pass
returncode=0
base=4 pre_count=4 post_count=5 switch_time_ns=40.250 |
| `multimod_divider_ratio_switch_smoke` | `unsupported/behavior_other` | `no_supported_signature` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:3
generated_include=multimod_divider_ratio_switch_ref.va
spectre_strict:preflight_pass
returncode=0
streaming_checker:not_enough_e |
| `nrz_prbs` | `unsupported/behavior_other` | `no_supported_signature` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:2
spectre_strict:preflight_pass
returncode=0
transitions=0 complement_err=0.0009 swing=0.200 |
| `pfd_deadzone_smoke` | `compile/preflight` | `compile_or_spectre_strict` | `FAIL_TB_COMPILE` | contract_save_pruned=removed:1,inserted:1,signals:4
generated_include=pfd_updn.va
spectre_strict:malformed_pwl_wave=15:tokens=365:Vdiv (div 0) vsource type=pwl wave=[0n 0 \ |
| `pfd_reset_race_smoke` | `onehot/thermometer/no-overlap` | `onehot_overlap_or_pointer` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:4
generated_include=pfd_updn.va
spectre_strict:preflight_pass
returncode=0
streaming_checker:up_first=0.0000 dn_first=0.0000 up_se |
| `phase_accumulator_timer_wrap_smoke` | `PFD/PLL timing_window` | `pulse_phase_lock_window` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:2
generated_include=phase_accumulator_timer_wrap_ref.va
spectre_strict:preflight_pass
returncode=0
wraps=0 clk_rises=1 phase_span= |
| `prbs7` | `unsupported/behavior_other` | `no_supported_signature` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:11
spectre_strict:preflight_pass
returncode=0
transitions=0 hi_frac=0.000 |
| `ramp_gen_smoke` | `unsupported/behavior_other` | `no_supported_signature` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:6
generated_include=ramp_gen.va
spectre_strict:preflight_pass
returncode=0
code_start=0 code_end=9 |
| `sample_hold_droop_smoke` | `sampled_latch/reset_priority` | `sample_or_q_mismatch` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:1,inserted:1,signals:3
generated_include=sample_hold_droop_ref.va
spectre_strict:preflight_pass
returncode=0
sample_mismatch=4/6 |
| `sar_adc_dac_weighted_8b_smoke` | `quantizer/code_coverage` | `code_coverage_or_unique_codes` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:3,inserted:1,signals:13
generated_include=sar_adc_weighted_8b.va
generated_include=dac_weighted_8b.va
generated_include=sh_ideal.va
spectre_strict:pref |
| `serializer_frame_alignment_smoke` | `frame/sequence_alignment` | `frame_or_sequence` | `FAIL_SIM_CORRECTNESS` | contract_save_pruned=removed:3,inserted:1,signals:12
generated_include=serializer_frame_alignment_ref.va
spectre_strict:preflight_pass
returncode=0
frame_rises=1 |
