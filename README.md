# BiasBench: A reproducible benchmark for tuning the biases of event cameras

The BiasBench dataset is a large-scale event camera dataset designed to evaluate the impact of bias parameters (ON/OFF) on event-based vision.

The total dateset contains<br>
- ~32,000 files<br>
- ~13 TB total size<br>
- Multiple datasets with structured bias parameter sweeps

Because of its size, the dataset is organized to allow selective downloading of relevant subsets.

## Dateset Structure
The dataset is organized hierarchically:<br>

biasbench/<br>
├── led/<br>
│   ├── data_set/<br>
│   ├── validation_set_files/<br>
├── robot_arm/<br>
│   ├── left_right_sorted/<br>
│   ├── triangle_sorted/<br>
├── spinning_dot/<br>
│   ├── black_dot/<br>
│   ├── grey_dot/<br>

### Grouping Concept
Each dataset is subdivided into:

Groups: group_X_Y<br>
Bias combinations: <bias_on>\_<bias_off>\_<bias_fo>\_<bias_hpf>\_<bias_refr>.hdf5

### Grouping Numbers


---

<details>
<summary>led dataset structure</summary>
    
<details>
<summary>group_0_0</summary>
--  100_150_...<br>
--  100_170_...<br>
--  120_150_...<br>
--  120_170_...<br>
</details>

<details>
<summary>group_0_1</summary>
--  100_110_...<br>
--  100_130_...<br>
--  120_110_...<br>
--  120_130_...<br>
</details>

<details>
<summary>group_0_2</summary>
--  100_70_...<br>
--  100_90_...<br>
--  120_70_...<br>
--  120_90_...<br>
</details>

<details>
<summary>group_0_3</summary>
--  100_30_...<br>
--  100_50_...<br>
--  120_30_...<br>
--  120_50_...<br>
</details>

<details>
<summary>group_0_4</summary>
--  100_-10_...<br>
--  100_10_...<br>
--  120_-10_...<br>
--  120_10_...<br>
</details>

<details>
<summary>group_0_5</summary>
--  100_-30_...<br>
--  120_-30_...<br>
--  60_-30_...<br>
--  80_-30_...<br>
</details>

<details>
<summary>group_1_0</summary>
--  60_150_...<br>
--  60_170_...<br>
--  80_150_...<br>
--  80_170_...<br>
</details>

<details>
<summary>group_1_1</summary>
--  60_110_...<br>
--  60_130_...<br>
--  80_110_...<br>
--  80_130_...<br>
</details>

<details>
<summary>group_1_2</summary>
--  60_70_...<br>
--  60_90_...<br>
--  80_70_...<br>
--  80_90_...<br>
</details>

<details>
<summary>group_1_3</summary>
--  60_30_...<br>
--  60_50_...<br>
--  80_30_...<br>
--  80_50_...<br>
</details>

<details>
<summary>group_1_4</summary>
--  60_-10_...<br>
--  60_10_...<br>
--  80_-10_...<br>
--  80_10_...<br>
</details>

<details>
<summary>group_1_5</summary>
--  -20_-30_...<br>
--  0_-30_...<br>
--  20_-30_...<br>
--  40_-30_...<br>
</details>

<details>
<summary>group_2_0</summary>
--  20_150_...<br>
--  20_170_...<br>
--  40_150_...<br>
--  40_170_...<br>
</details>

<details>
<summary>group_2_1</summary>
--  20_110_...<br>
--  20_130_...<br>
--  40_110_...<br>
--  40_130_...<br>
</details>

<details>
<summary>group_2_2</summary>
--  20_70_...<br>
--  20_90_...<br>
--  40_70_...<br>
--  40_90_...<br>
</details>

<details>
<summary>group_2_3</summary>
--  20_30_...<br>
--  20_50_...<br>
--  40_30_...<br>
--  40_50_...<br>
</details>

<details>
<summary>group_2_4</summary>
--  20_-10_...<br>
--  20_10_...<br>
--  40_-10_...<br>
--  40_10_...<br>
</details>

<details>
<summary>group_3_0</summary>
--  -20_150_...<br>
--  -20_170_...<br>
--  0_150_...<br>
--  0_170_...<br>
</details>

<details>
<summary>group_3_1</summary>
--  -20_110_...<br>
--  -20_130_...<br>
--  0_110_...<br>
--  0_130_...<br>
</details>

<details>
<summary>group_3_2</summary>
--  -20_70_...<br>
--  -20_90_...<br>
--  0_70_...<br>
--  0_90_...<br>
</details>

<details>
<summary>group_3_3</summary>
--  -20_30_...<br>
--  -20_50_...<br>
--  0_30_...<br>
--  0_50_...<br>
</details>

<details>
<summary>group_3_4</summary>
--  -20_-10_...<br>
--  -20_10_...<br>
--  0_-10_...<br>
--  0_10_...<br>
</details>

<details>
<summary>group_4_0</summary>
--  -40_150_...<br>
--  -40_170_...<br>
--  -60_150_...<br>
--  -60_170_...<br>
</details>

<details>
<summary>group_4_1</summary>
--  -40_110_...<br>
--  -40_130_...<br>
--  -60_110_...<br>
--  -60_130_...<br>
</details>

<details>
<summary>group_4_2</summary>
--  -40_70_...<br>
--  -40_90_...<br>
--  -60_70_...<br>
--  -60_90_...<br>
</details>

<details>
<summary>group_4_3</summary>
--  -40_30_...<br>
--  -40_50_...<br>
--  -60_30_...<br>
--  -60_50_...<br>
</details>

<details>
<summary>group_4_4</summary>
--  -40_-10_...<br>
--  -40_10_...<br>
--  -60_-10_...<br>
--  -60_10_...<br>
</details>

<details>
<summary>group_5_0</summary>
--  -80_110_...<br>
--  -80_130_...<br>
--  -80_150_...<br>
--  -80_170_...<br>
</details>

<details>
<summary>group_5_1</summary>
--  -80_30_...<br>
--  -80_50_...<br>
--  -80_70_...<br>
--  -80_90_...<br>
</details>

<details>
<summary>group_5_5</summary>
--  -40_-30_...<br>
--  -60_-30_...<br>
--  -80_-10_...<br>
--  -80_-30_...<br>
--  -80_10_...<br>
</details>
</details>



<details>
<summary>robotic arm dataset structure</summary>
    
<details>
<summary>group_0_0</summary>
--  112_132_...<br>
--  112_147_...<br>
--  112_161_...<br>
--  112_175_...<br>
--  112_190_...<br>
--  126_132_...<br>
--  126_147_...<br>
--  126_161_...<br>
--  126_175_...<br>
--  126_190_...<br>
--  140_132_...<br>
--  140_147_...<br>
--  140_161_...<br>
--  140_175_...<br>
--  140_190_...<br>
--  85_132_...<br>
--  85_147_...<br>
--  85_161_...<br>
--  85_175_...<br>
--  85_190_...<br>
--  99_132_...<br>
--  99_147_...<br>
--  99_161_...<br>
--  99_175_...<br>
--  99_190_...<br>
</details>

<details>
<summary>group_0_1</summary>
--  112_104_...<br>
--  112_118_...<br>
--  112_61_...<br>
--  112_75_...<br>
--  112_90_...<br>
--  126_104_...<br>
--  126_118_...<br>
--  126_61_...<br>
--  126_75_...<br>
--  126_90_...<br>
--  140_104_...<br>
--  140_118_...<br>
--  140_61_...<br>
--  140_75_...<br>
--  140_90_...<br>
--  85_104_...<br>
--  85_118_...<br>
--  85_61_...<br>
--  85_75_...<br>
--  85_90_...<br>
--  99_104_...<br>
--  99_118_...<br>
--  99_61_...<br>
--  99_75_...<br>
--  99_90_...<br>
</details>

<details>
<summary>group_0_2</summary>
--  112_-10_...<br>
--  112_18_...<br>
--  112_32_...<br>
--  112_47_...<br>
--  112_4_...<br>
--  126_-10_...<br>
--  126_18_...<br>
--  126_32_...<br>
--  126_47_...<br>
--  126_4_...<br>
--  140_-10_...<br>
--  140_18_...<br>
--  140_32_...<br>
--  140_47_...<br>
--  140_4_...<br>
--  85_-10_...<br>
--  85_18_...<br>
--  85_32_...<br>
--  85_47_...<br>
--  85_4_...<br>
--  99_-10_...<br>
--  99_18_...<br>
--  99_32_...<br>
--  99_47_...<br>
--  99_4_...<br>
</details>

<details>
<summary>group_1_0</summary>
--  17_132_...<br>
--  17_147_...<br>
--  17_161_...<br>
--  17_175_...<br>
--  17_190_...<br>
--  31_132_...<br>
--  31_147_...<br>
--  31_161_...<br>
--  31_175_...<br>
--  31_190_...<br>
--  45_132_...<br>
--  45_147_...<br>
--  45_161_...<br>
--  45_175_...<br>
--  45_190_...<br>
--  58_132_...<br>
--  58_147_...<br>
--  58_161_...<br>
--  58_175_...<br>
--  58_190_...<br>
--  72_132_...<br>
--  72_147_...<br>
--  72_161_...<br>
--  72_175_...<br>
--  72_190_...<br>
</details>

<details>
<summary>group_1_1</summary>
--  17_104_...<br>
--  17_118_...<br>
--  17_61_...<br>
--  17_75_...<br>
--  17_90_...<br>
--  31_104_...<br>
--  31_118_...<br>
--  31_61_...<br>
--  31_75_...<br>
--  31_90_...<br>
--  45_104_...<br>
--  45_118_...<br>
--  45_61_...<br>
--  45_75_...<br>
--  45_90_...<br>
--  58_104_...<br>
--  58_118_...<br>
--  58_61_...<br>
--  58_75_...<br>
--  58_90_...<br>
--  72_104_...<br>
--  72_118_...<br>
--  72_61_...<br>
--  72_75_...<br>
--  72_90_...<br>
</details>

<details>
<summary>group_1_2</summary>
--  17_-10_...<br>
--  17_18_...<br>
--  17_32_...<br>
--  17_47_...<br>
--  17_4_...<br>
--  31_-10_...<br>
--  31_18_...<br>
--  31_32_...<br>
--  31_47_...<br>
--  31_4_...<br>
--  45_-10_...<br>
--  45_18_...<br>
--  45_32_...<br>
--  45_47_...<br>
--  45_4_...<br>
--  58_-10_...<br>
--  58_18_...<br>
--  58_32_...<br>
--  58_47_...<br>
--  58_4_...<br>
--  72_-10_...<br>
--  72_18_...<br>
--  72_32_...<br>
--  72_47_...<br>
--  72_4_...<br>
</details>

<details>
<summary>group_2_0</summary>
--  -22_132_...<br>
--  -22_147_...<br>
--  -22_161_...<br>
--  -22_175_...<br>
--  -22_190_...<br>
--  -36_132_...<br>
--  -36_147_...<br>
--  -36_161_...<br>
--  -36_175_...<br>
--  -36_190_...<br>
--  -50_132_...<br>
--  -50_147_...<br>
--  -50_161_...<br>
--  -50_175_...<br>
--  -50_190_...<br>
--  -9_132_...<br>
--  -9_147_...<br>
--  -9_161_...<br>
--  -9_175_...<br>
--  -9_190_...<br>
--  4_132_...<br>
--  4_147_...<br>
--  4_161_...<br>
--  4_175_...<br>
--  4_190_...<br>
</details>

<details>
<summary>group_2_1</summary>
--  -22_104_...<br>
--  -22_118_...<br>
--  -22_61_...<br>
--  -22_75_...<br>
--  -22_90_...<br>
--  -36_104_...<br>
--  -36_118_...<br>
--  -36_61_...<br>
--  -36_75_...<br>
--  -36_90_...<br>
--  -50_104_...<br>
--  -50_118_...<br>
--  -50_61_...<br>
--  -50_75_...<br>
--  -50_90_...<br>
--  -9_104_...<br>
--  -9_118_...<br>
--  -9_61_...<br>
--  -9_75_...<br>
--  -9_90_...<br>
--  4_104_...<br>
--  4_118_...<br>
--  4_61_...<br>
--  4_75_...<br>
--  4_90_...<br>
</details>

<details>
<summary>group_2_2</summary>
--  -22_-10_...<br>
--  -22_18_...<br>
--  -22_32_...<br>
--  -22_47_...<br>
--  -22_4_...<br>
--  -36_-10_...<br>
--  -36_18_...<br>
--  -36_32_...<br>
--  -36_47_...<br>
--  -36_4_...<br>
--  -50_-10_...<br>
--  -50_18_...<br>
--  -50_32_...<br>
--  -50_47_...<br>
--  -50_4_...<br>
--  -9_-10_...<br>
--  -9_18_...<br>
--  -9_32_...<br>
--  -9_47_...<br>
--  -9_4_...<br>
--  4_-10_...<br>
--  4_18_...<br>
--  4_32_...<br>
--  4_47_...<br>
--  4_4_...<br>
</details>
</details>


<details>
<summary>spinning dot dataset structure</summary>
    
<details>
<summary>group_0_0</summary>
--  130_178_...<br>
--  130_190_...<br>
--  140_178_...<br>
--  140_190_...<br>
</details>

<details>
<summary>group_0_1</summary>
--  130_154_...<br>
--  130_166_...<br>
--  140_154_...<br>
--  140_166_...<br>
</details>

<details>
<summary>group_0_2</summary>
--  130_131_...<br>
--  130_142_...<br>
--  140_131_...<br>
--  140_142_...<br>
</details>

<details>
<summary>group_0_3</summary>
--  130_107_...<br>
--  130_119_...<br>
--  140_107_...<br>
--  140_119_...<br>
</details>

<details>
<summary>group_0_4</summary>
--  130_84_...<br>
--  130_95_...<br>
--  140_84_...<br>
--  140_95_...<br>
</details>

<details>
<summary>group_0_5</summary>
--  130_60_...<br>
--  130_72_...<br>
--  140_60_...<br>
--  140_72_...<br>
</details>

<details>
<summary>group_0_6</summary>
--  130_37_...<br>
--  130_48_...<br>
--  140_37_...<br>
--  140_48_...<br>
</details>

<details>
<summary>group_0_7</summary>
--  130_13_...<br>
--  130_25_...<br>
--  140_13_...<br>
--  140_25_...<br>
</details>

<details>
<summary>group_0_8</summary>
--  130_-10_...<br>
--  130_1_...<br>
--  140_-10_...<br>
--  140_1_...<br>
</details>

<details>
<summary>group_1_0</summary>
--  110_178_...<br>
--  110_190_...<br>
--  120_178_...<br>
--  120_190_...<br>
</details>

<details>
<summary>group_1_1</summary>
--  110_154_...<br>
--  110_166_...<br>
--  120_154_...<br>
--  120_166_...<br>
</details>

<details>
<summary>group_1_2</summary>
--  110_131_...<br>
--  110_142_...<br>
--  120_131_...<br>
--  120_142_...<br>
</details>

<details>
<summary>group_1_3</summary>
--  110_107_...<br>
--  110_119_...<br>
--  120_107_...<br>
--  120_119_...<br>
</details>

<details>
<summary>group_1_4</summary>
--  110_84_...<br>
--  110_95_...<br>
--  120_84_...<br>
--  120_95_...<br>
</details>

<details>
<summary>group_1_5</summary>
--  110_60_...<br>
--  110_72_...<br>
--  120_60_...<br>
--  120_72_...<br>
</details>

<details>
<summary>group_1_6</summary>
--  110_37_...<br>
--  110_48_...<br>
--  120_37_...<br>
--  120_48_...<br>
</details>

<details>
<summary>group_1_7</summary>
--  110_13_...<br>
--  110_25_...<br>
--  120_13_...<br>
--  120_25_...<br>
</details>

<details>
<summary>group_1_8</summary>
--  110_-10_...<br>
--  110_1_...<br>
--  120_-10_...<br>
--  120_1_...<br>
</details>

<details>
<summary>group_2_0</summary>
--  100_178_...<br>
--  100_190_...<br>
--  90_178_...<br>
--  90_190_...<br>
</details>

<details>
<summary>group_2_1</summary>
--  100_154_...<br>
--  100_166_...<br>
--  90_154_...<br>
--  90_166_...<br>
</details>

<details>
<summary>group_2_2</summary>
--  100_131_...<br>
--  100_142_...<br>
--  90_131_...<br>
--  90_142_...<br>
</details>

<details>
<summary>group_2_3</summary>
--  100_107_...<br>
--  100_119_...<br>
--  90_107_...<br>
--  90_119_...<br>
</details>

<details>
<summary>group_2_4</summary>
--  100_84_...<br>
--  100_95_...<br>
--  90_84_...<br>
--  90_95_...<br>
</details>

<details>
<summary>group_2_5</summary>
--  100_60_...<br>
--  100_72_...<br>
--  90_60_...<br>
--  90_72_...<br>
</details>

<details>
<summary>group_2_6</summary>
--  100_37_...<br>
--  100_48_...<br>
--  90_37_...<br>
--  90_48_...<br>
</details>

<details>
<summary>group_2_7</summary>
--  100_13_...<br>
--  100_25_...<br>
--  90_13_...<br>
--  90_25_...<br>
</details>

<details>
<summary>group_2_8</summary>
--  100_-10_...<br>
--  100_1_...<br>
--  90_-10_...<br>
--  90_1_...<br>
</details>

<details>
<summary>group_3_0</summary>
--  70_178_...<br>
--  70_190_...<br>
--  80_178_...<br>
--  80_190_...<br>
</details>

<details>
<summary>group_3_1</summary>
--  70_154_...<br>
--  70_166_...<br>
--  80_154_...<br>
--  80_166_...<br>
</details>

<details>
<summary>group_3_2</summary>
--  70_131_...<br>
--  70_142_...<br>
--  80_131_...<br>
--  80_142_...<br>
</details>

<details>
<summary>group_3_3</summary>
--  70_107_...<br>
--  70_119_...<br>
--  80_107_...<br>
--  80_119_...<br>
</details>

<details>
<summary>group_3_4</summary>
--  70_84_...<br>
--  70_95_...<br>
--  80_84_...<br>
--  80_95_...<br>
</details>

<details>
<summary>group_3_5</summary>
--  70_60_...<br>
--  70_72_...<br>
--  80_60_...<br>
--  80_72_...<br>
</details>

<details>
<summary>group_3_6</summary>
--  70_37_...<br>
--  70_48_...<br>
--  80_37_...<br>
--  80_48_...<br>
</details>

<details>
<summary>group_3_7</summary>
--  70_13_...<br>
--  70_25_...<br>
--  80_13_...<br>
--  80_25_...<br>
</details>

<details>
<summary>group_3_8</summary>
--  70_-10_...<br>
--  70_1_...<br>
--  80_-10_...<br>
--  80_1_...<br>
</details>

<details>
<summary>group_4_0</summary>
--  50_178_...<br>
--  50_190_...<br>
--  60_178_...<br>
--  60_190_...<br>
</details>

<details>
<summary>group_4_1</summary>
--  50_154_...<br>
--  50_166_...<br>
--  60_154_...<br>
--  60_166_...<br>
</details>

<details>
<summary>group_4_2</summary>
--  50_131_...<br>
--  50_142_...<br>
--  60_131_...<br>
--  60_142_...<br>
</details>

<details>
<summary>group_4_3</summary>
--  50_107_...<br>
--  50_119_...<br>
--  60_107_...<br>
--  60_119_...<br>
</details>

<details>
<summary>group_4_4</summary>
--  50_84_...<br>
--  50_95_...<br>
--  60_84_...<br>
--  60_95_...<br>
</details>

<details>
<summary>group_4_5</summary>
--  50_60_...<br>
--  50_72_...<br>
--  60_60_...<br>
--  60_72_...<br>
</details>

<details>
<summary>group_4_6</summary>
--  50_37_...<br>
--  50_48_...<br>
--  60_37_...<br>
--  60_48_...<br>
</details>

<details>
<summary>group_4_7</summary>
--  50_13_...<br>
--  50_25_...<br>
--  60_13_...<br>
--  60_25_...<br>
</details>

<details>
<summary>group_4_8</summary>
--  50_-10_...<br>
--  50_1_...<br>
--  60_-10_...<br>
--  60_1_...<br>
</details>

<details>
<summary>group_5_0</summary>
--  30_178_...<br>
--  30_190_...<br>
--  40_178_...<br>
--  40_190_...<br>
</details>

<details>
<summary>group_5_1</summary>
--  30_154_...<br>
--  30_166_...<br>
--  40_154_...<br>
--  40_166_...<br>
</details>

<details>
<summary>group_5_2</summary>
--  30_131_...<br>
--  30_142_...<br>
--  40_131_...<br>
--  40_142_...<br>
</details>

<details>
<summary>group_5_3</summary>
--  30_107_...<br>
--  30_119_...<br>
--  40_107_...<br>
--  40_119_...<br>
</details>

<details>
<summary>group_5_4</summary>
--  30_84_...<br>
--  30_95_...<br>
--  40_84_...<br>
--  40_95_...<br>
</details>

<details>
<summary>group_5_5</summary>
--  30_60_...<br>
--  30_72_...<br>
--  40_60_...<br>
--  40_72_...<br>
</details>

<details>
<summary>group_5_6</summary>
--  30_37_...<br>
--  30_48_...<br>
--  40_37_...<br>
--  40_48_...<br>
</details>

<details>
<summary>group_5_7</summary>
--  30_13_...<br>
--  30_25_...<br>
--  40_13_...<br>
--  40_25_...<br>
</details>

<details>
<summary>group_5_8</summary>
--  30_-10_...<br>
--  30_1_...<br>
--  40_-10_...<br>
--  40_1_...<br>
</details>

<details>
<summary>group_6_0</summary>
--  10_178_...<br>
--  10_190_...<br>
--  20_178_...<br>
--  20_190_...<br>
</details>

<details>
<summary>group_6_1</summary>
--  10_154_...<br>
--  10_166_...<br>
--  20_154_...<br>
--  20_166_...<br>
</details>

<details>
<summary>group_6_2</summary>
--  10_131_...<br>
--  10_142_...<br>
--  20_131_...<br>
--  20_142_...<br>
</details>

<details>
<summary>group_6_3</summary>
--  10_107_...<br>
--  10_119_...<br>
--  20_107_...<br>
--  20_119_...<br>
</details>

<details>
<summary>group_6_4</summary>
--  10_84_...<br>
--  10_95_...<br>
--  20_84_...<br>
--  20_95_...<br>
</details>

<details>
<summary>group_6_5</summary>
--  10_60_...<br>
--  10_72_...<br>
--  20_60_...<br>
--  20_72_...<br>
</details>

<details>
<summary>group_6_6</summary>
--  10_37_...<br>
--  10_48_...<br>
--  20_37_...<br>
--  20_48_...<br>
</details>

<details>
<summary>group_6_7</summary>
--  10_13_...<br>
--  10_25_...<br>
--  20_13_...<br>
--  20_25_...<br>
</details>

<details>
<summary>group_6_8</summary>
--  10_-10_...<br>
--  10_1_...<br>
--  20_-10_...<br>
--  20_1_...<br>
</details>

<details>
<summary>group_7_0</summary>
--  -10_178_...<br>
--  -10_190_...<br>
--  0_178_...<br>
--  0_190_...<br>
</details>

<details>
<summary>group_7_1</summary>
--  -10_154_...<br>
--  -10_166_...<br>
--  0_154_...<br>
--  0_166_...<br>
</details>

<details>
<summary>group_7_2</summary>
--  -10_131_...<br>
--  -10_142_...<br>
--  0_131_...<br>
--  0_142_...<br>
</details>

<details>
<summary>group_7_3</summary>
--  -10_107_...<br>
--  -10_119_...<br>
--  0_107_...<br>
--  0_119_...<br>
</details>

<details>
<summary>group_7_4</summary>
--  -10_84_...<br>
--  -10_95_...<br>
--  0_84_...<br>
--  0_95_...<br>
</details>

<details>
<summary>group_7_5</summary>
--  -10_60_...<br>
--  -10_72_...<br>
--  0_60_...<br>
--  0_72_...<br>
</details>

<details>
<summary>group_7_6</summary>
--  -10_37_...<br>
--  -10_48_...<br>
--  0_37_...<br>
--  0_48_...<br>
</details>

<details>
<summary>group_7_7</summary>
--  -10_13_...<br>
--  -10_25_...<br>
--  0_13_...<br>
--  0_25_...<br>
</details>

<details>
<summary>group_7_8</summary>
--  -10_-10_...<br>
--  -10_1_...<br>
--  0_-10_...<br>
--  0_1_...<br>
</details>

<details>
<summary>group_8_0</summary>
--  -20_178_...<br>
--  -20_190_...<br>
--  -30_178_...<br>
--  -30_190_...<br>
</details>

<details>
<summary>group_8_1</summary>
--  -20_154_...<br>
--  -20_166_...<br>
--  -30_154_...<br>
--  -30_166_...<br>
</details>

<details>
<summary>group_8_2</summary>
--  -20_131_...<br>
--  -20_142_...<br>
--  -30_131_...<br>
--  -30_142_...<br>
</details>

<details>
<summary>group_8_3</summary>
--  -20_107_...<br>
--  -20_119_...<br>
--  -30_107_...<br>
--  -30_119_...<br>
</details>

<details>
<summary>group_8_4</summary>
--  -20_84_...<br>
--  -20_95_...<br>
--  -30_84_...<br>
--  -30_95_...<br>
</details>

<details>
<summary>group_8_5</summary>
--  -20_60_...<br>
--  -20_72_...<br>
--  -30_60_...<br>
--  -30_72_...<br>
</details>

<details>
<summary>group_8_6</summary>
--  -20_37_...<br>
--  -20_48_...<br>
--  -30_37_...<br>
--  -30_48_...<br>
</details>

<details>
<summary>group_8_7</summary>
--  -20_13_...<br>
--  -20_25_...<br>
--  -30_13_...<br>
--  -30_25_...<br>
</details>

<details>
<summary>group_8_8</summary>
--  -20_-10_...<br>
--  -20_1_...<br>
--  -30_-10_...<br>
--  -30_1_...<br>
</details>
</details>




<p></p>

## Data Download

wget can be used to download the dataset.

### Full Dataset Download

To download the full dataset use:<br>
```
wget -r -c -np -nH ??urls
```
<p>

To download a specific dataset use:

```
wget -r -c -np -nH ??urls/<datasetname>
```
<p>

To download a specific group use:

```
wget -r -c -np -nH ??urls/<datasetname>/<groupname>
```
<p>

To download a specific file use:

```
wget -r -c -np -nH ??urls/<datasetname>/<groupname>/<filename>
```
<p>


### Predefined Groups

For easier Managability 3 predefiined groups are already selected:
- small: containing files with the most common bias values
- medium: additionally containing verry high biases 
- large: containing all but the lowest bias configurations


| Size | bias_on min| bias_on max | bias_off min | bias_off max|
| ----------- | ----------- |----------- |----------- |----------- |
| small | -20| 80|30|130|
| medium |  -20| - |30 | - |
| large |   -70| - |-20 | - |


| Size | LED data| LED validation | Robot Arm Left Right | Robot Arm Triangle| Spinning Dot Black| Spinning Dot Grey|
| ----------- | ----------- |----------- |----------- |----------- |----------- |----------- |
| small | 289GB|554GB | 184GB|143GB  | 230GB|102GB |
| medium | 431GB|789GB |  318GB|254GB | 445GB|156GB |
| large | 1881GB|2552GB |  776GB|665GB | 762GB|361GB |
| full | 4834GB|5582GB | 776GB|665GB  | 762GB|361GB |


For downloading the small dataset use:
```
wget -r -c -np -nH --accept-regex='.*/(-20|-1?[0-9]|[0-7]?[0-9]|80)_([3-9][0-9]|1[0-2][0-9]|130)_.*' URL_TO_LED_DATASET
```

For downloading the medium dataset use:
```
wget -r -c -np -nH --accept-regex='.*/(-20|-1?[0-9]|[0-9]?[0-9]|1[0-2][0-9]|130)_([3-9][0-9]|1[0-7][0-9]|180)_.*' URL_TO_LED_DATASET
```

For downloading the large dataset use:
```
wget -r -c -np -nH --accept-regex='.*/(-70|-[1-6]?[0-9]|[0-9]?[0-9]|1[0-2][0-9]|130)_(-20|-1?[0-9]|[0-9]?[0-9]|1[0-7][0-9]|180)_.*' URL_TO_LED_DATASET
```
### Download per File

The file `biasbench_downloader.sh` is capable fo doenloading more specific parts of the Dataset.


To do so download the file and make it executable. Afterwards you can choose from several download modes:<p>
\<dataset\> can hereby be one of:


- led<br>
- led/data_set<br>
- led/validation_set_files<br>
- robot_arm<br>
- robot_arm/left_right_sorted<br>
- robot_arm/triangle_sorted<br>
- spinning_dot<br>
- spinning_dot/black_dot<br>
- spinning_dot/grey_dot<br>

\<range\> can be one of:
- min:max (20-80)<br>
- :max (:80) = (-inf : 80) <br>
- min: (20:) = (20 : inf)<br>
-  :   (:) = (-inf : inf)<br>

non stated ranges will be interpreted as : 




Download the same Grouping from all Datasets:

```
./biasbench_downloader.sh <size>
```

Download the same Grouping from specific Datasets:

```
./biasbench_downloader.sh <size> <dataset1,dataset2,....>
```

Download specific Biasranges from all datasets:

```
./biasbench_downloader.sh all [<range_on>,<range_off>,<range_fo>,<range_hpf>,<range_refr>]
```

Download specific Biasranges from specific datasets:

```
./biasbench_downloader.sh <dataset1,dataset2,....> [<range_on>,<range_off>,<range_fo>,<range_hpf>,<range_refr>]
```
