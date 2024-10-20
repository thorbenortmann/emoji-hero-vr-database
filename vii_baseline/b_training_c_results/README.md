# VII.B_C. Training and Results

You can find the training script for each model mentioned in subsection `VII.C. Results` of our paper
[EmojiHeroVR: A Study on Facial Expression Recognition under Partial Occlusion from Head-Mounted Displays](https://doi.org/10.48550/arXiv.2410.03331)
in the subdirectories of this directory:

- Table III - AffectNet
    - AffectNet without Occlusion: [affectnet_7](./affectnet_7) -
      Model: https://drive.google.com/file/d/1RtPzrQpG3OrrOVUPCbNdI1d7e2hPGKyh/view?usp=sharing
    - AffectNet with Occlusion: [affectnet_7_occl](./affectnet_7_occl) -
      Model: https://drive.google.com/file/d/1ziHE4puz1xq0LWOPBalBuVrPIAjdHs4p/view?usp=sharing


- Table IV - KDEF and EmoHeVRDB
    - KDEF-SHR: [kdef_shr](./kdef_shr) -
      Model: https://drive.google.com/file/d/1_mMsi8WsECWMS953i_HAAa7YQpV1nave/view?usp=sharing
    - KDEF-SHR-occl: [kdef_shr_occl](./kdef_shr_occl) -
      Model: https://drive.google.com/file/d/12HZEhVCEkNwRDNW2IO42qzu1AEZhw2GG/view?usp=sharing
    - EmoHeVRDB: [emohevrdb](emohevrdb) -
      Model: https://drive.google.com/file/d/1dWeQEf4VkhsVXUWwITMN09Ya-cBVsuNY/view?usp=sharing


- Table V - Cross-Dataset Evaluations
    - AffectNet-7 -> KDEF-SHR: [affectnet_7_kdef_shr](./cross_dataset_evaluation/affectnet_7_kdef_shr)
    - AffectNet-7 -> KDEF-SHR-oocl: [affectnet_7_kdef_shr_occl](./cross_dataset_evaluation/affectnet_7_kdef_shr_occl)
    - AffectNet-7-occl ->
      KDEF-SHR-oocl: [affectnet_7_occl_kdef_shr_occl](./cross_dataset_evaluation/affectnet_7_occl_kdef_shr_occl)
    - AffectNet-7 -> EmoHeVRDB: [affectnet_7_emohevrdb](./cross_dataset_evaluation/affectnet_7_emohevrdb)
      EmoHeVRDB: [affectnet_7_occl_emohevrdb](./cross_dataset_evaluation/affectnet_7_occl_emohevrdb)
    - AffectNet-7-occl & EmoHeVRDB ->
      EmoHeVRDB: [affectnet_7_occl_emohevrdb](./cross_dataset_evaluation/affectnet_7_occl_emohevrdb) - Models:
        - 1_to_1: https://drive.google.com/file/d/1fWG1iGOUNSRoCZz-FaYdaYQEnbAGY5Dd/view?usp=sharing
        - 1_to_4: https://drive.google.com/file/d/1hg4dD0Qcfpi4Ra0LO-coQywri7HTZNcf/view?usp=sharing
