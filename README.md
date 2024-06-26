  
# AutoPMD
## Project Introduction  
**AutoPMD** is automated point mutation primer design tool for high-throughput protein modification.
![AutoPMD](https://github.com/editSeqDesign/AutoPMD/blob/main/img/home.png) 
## The main application scenarios of this software tool include:
### 1. Single point mutation primer design
- **Description**：Support the design of primers for implementing single amino acid point mutations.
### 2. Double point mutation primer design
- **Description**：Support the design of primers for implementing mutations at two amino acid sites.
    - The distance between amino acid sites of two mutations is less than or equal to 15bp
    - The distance between amino acid sites of two mutations is greater than 15bp but less than or equal to 120bp
    - The distance between amino acid sites of two mutations is greater than 120bp

  
## Installation
### python packages
We suggest using Python 3.8 for AutoPMD.

```shell
pip install -r requirements.txt

```


## Usage & Example

**Input:**
- **Step 1:** Upload the plasmid template(gb) file and the target information(CSV) file to be edited.
- **Step 2:** provide the necessary configuration information.
    - Example configuration (params.json):
      ```json
      {
      "pcr_single_primer_params":{
          "PRIMER_OPT_SIZE": 29,
          "PRIMER_MIN_SIZE": 27,
          "PRIMER_MAX_SIZE": 36,
          "PRIMER_OPT_TM": 65.0,
          "PRIMER_MIN_TM": 60.0,
          "PRIMER_MAX_TM": 75.0,
          "PRIMER_MIN_GC": 20.0,
          "PRIMER_MAX_GC": 80.0
          },
      "pcr_double_primer_params":{
          "PRIMER_OPT_SIZE": 29,  
          "PRIMER_MIN_SIZE": 27,
          "PRIMER_MAX_SIZE": 36,
          "PRIMER_OPT_TM": 65.0,
          "PRIMER_MIN_TM": 60.0,
          "PRIMER_MAX_TM": 75.0,
          "PRIMER_MIN_GC": 20.0,
          "PRIMER_MAX_GC": 80.0
      },
      "seq_primer_params":{
          "PRIMER_OPT_SIZE": 20,
          "PRIMER_MIN_SIZE": 18,
          "PRIMER_MAX_SIZE": 25,
          "PRIMER_OPT_TM": 65.0,
          "PRIMER_MIN_TM": 55.0,
          "PRIMER_MAX_TM": 75.0,
          "PRIMER_MIN_GC": 20,
          "PRIMER_MAX_GC": 80  
        },
      "global_params":{
          "AMPLICONIC_MARKER_SEQ_START_LENGTH": [200,100],
          "AMPLICONIC_GENE_TARGET_SEQ_LENGTH": 40    
      },   
      "input_mute_name":"自动化构建的样品引物设计.xlsx",  
      "inputdir":"/input_mut/",
      "outputdir":"/output/",
      "targetGene_after_before_seq_n":80
      }
      ```   
      

**Execute:**

```shell
python main.py  -i params.json
```
**Output:**
- `sucess_site_mute.zip` 
- `failture_site_mute.zip` 

These files will be generated in the `XXX/AutoPMD/src/data/output` directory.

