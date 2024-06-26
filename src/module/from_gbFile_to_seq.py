
from Bio import SeqIO
import pandas as pd
import sys,os
sys.path.append('../')
from utils.config import config  

# #质粒文件地址   
# plasmid_file_path = config.INPUT_FILE_PATH + 'target_gene_cross_ori.gb'
# # config.PLASMID_FILE_NAME
# genebank_db = SeqIO.read(plasmid_file_path, "genbank")   

     
#坐标转序列
def coordinate_2_seq(coordinate,seq):
    return str(seq[coordinate[0]:coordinate[1]])

#处理坐标
def deal_coordinate(obt,start,end,opt=0):
    if obt == 'target_gene':
        start = start - opt
        end = end + opt
    elif obt == 'marker':
        start = start + int(config.AMPLICONIC_MARKER_SEQ_START)
        end = start + opt
    elif obt =='marker_up_coordinate':
        start = start
        end = end 
    elif obt == 'marker_down_coordinate':   
        start = start+opt
        end =end-opt
    elif obt == 'target_gene_down_coordinate':
        start = start + opt
        end = end
    elif obt == 'target_gene1':
        start = start - opt
        end = end
    elif obt == 'target_gene2':
        start = start
        end = end + opt
    return start, end
    


#顺时针为准(即坐标为准),不考虑引物方向
def get_data_from_genebank(infile='icd-28a-new.gb',marker='KanR',target_gene='alsD-target gene'):
  
    genebank_db = SeqIO.read(infile, "genbank")    
   
    #取目标坐标
    start = genebank_db.features[0].location.start.position
    end = genebank_db.features[0].location.end.position

    #目标序列是否cross序列原点
    tag = 0 
    for ele in genebank_db.features:
        if ele.type == "CDS" and marker in ele.qualifiers['label']:
            marker_start = ele.location.start.position
            marker_end = ele.location.end.position
        elif ele.type == "CDS" and target_gene in ele.qualifiers['label']:
             
            target_gene_start = ele.location.start.position
            target_gene_end = ele.location.end.position
        elif ele.type == 'misc_feature' and target_gene in ele.qualifiers['label']:
            tag = 1   
            target_gene1_start = ele.location.parts[0].start.position
            target_gene1_end = ele.location.parts[0].end.position
            target_gene2_start = ele.location.parts[1].start.position
            target_gene2_end = ele.location.parts[1].end.position
        elif ele.type == 'misc_feature' and marker in ele.qualifiers['label']:
            tag = 2
            marker1_start = ele.location.parts[0].start.position
            marker1_end = ele.location.parts[0].end.position
            marker2_start = ele.location.parts[1].start.position
            marker2_end = ele.location.parts[1].end.position
        
    #取序列的四种情况，以零点为中心   
    #1.target_gene_seq在左，marker_seq在右
    #2.marker_seq在左，target_gene_seq在右
    #3.零点在target_gene_seq上
    #4.零点在marker_seq上
    if tag == 0 :                                                   #no crosss zero
        #处理目标                                                   
        target_gene_coordinate = deal_coordinate(
                                                    'target_gene',
                                                    target_gene_start,
                                                    target_gene_end,
                                                    opt=config.AMPLICONIC_GENE_TARGET_SEQ_LENGTH
                                                )
        marker_coordinate = deal_coordinate(
                                                'marker',
                                                marker_start,
                                                marker_end,
                                                opt=config.AMPLICONIC_MARKER_SEQ_LENGTH
                                        )
        #取序列
        target_gene_seq = coordinate_2_seq(target_gene_coordinate,seq=genebank_db.seq)
        marker_seq = coordinate_2_seq(marker_coordinate,seq=genebank_db.seq)

         #1.target_gene_seq在左，marker_seq在右    条件：
        if marker_coordinate[1] < target_gene_coordinate[0] and marker_coordinate[0] < target_gene_coordinate[0]: 
            marker_up_coordinate = deal_coordinate(
                                                        'marker_up_coordinate',
                                                        start,
                                                        marker_coordinate[0]
                                                    )
            marker_down_coordinate = deal_coordinate(
                                                        'marker_down_coordinate',
                                                        marker_coordinate[1],
                                                        target_gene_coordinate[0]
                                                    )
            target_gene_down_coordinate =  deal_coordinate(
                                                            'target_gene_down_coordinate',
                                                            target_gene_coordinate[1],
                                                            end
                                                        )
            #取序列
            target_gene_down_seq = ''.join([
                                        coordinate_2_seq(target_gene_down_coordinate,seq=genebank_db.seq),
                                        coordinate_2_seq(marker_up_coordinate,seq=genebank_db.seq)
                                        ])
            target_gene_up_seq =coordinate_2_seq(marker_down_coordinate,seq=genebank_db.seq)

        #2.marker_seq在左，target_gene_seq在右   条件：
        elif marker_coordinate[0] > target_gene_coordinate[1] and marker_coordinate[0] > target_gene_coordinate[0]:  

            marker_up_coordinate =  deal_coordinate(
                                                        'marker_up_coordinate',
                                                        target_gene_coordinate[1],
                                                        marker_coordinate[0]
                                                    )
            marker_down_coordinate = deal_coordinate(
                                                        'marker_down_coordinate',
                                                        marker_coordinate[1],
                                                        end
                                                    )
            target_gene_up_coordinate =  deal_coordinate(
                                                            'target_gene_down_coordinate',
                                                            start,
                                                            target_gene_coordinate[0]
                                                        )
            #取序列
            target_gene_up_seq = ''.join([
                                        coordinate_2_seq(marker_down_coordinate,seq=genebank_db.seq),
                                        coordinate_2_seq(target_gene_up_coordinate,seq=genebank_db.seq)
                                        ])
            target_gene_down_seq =coordinate_2_seq(marker_up_coordinate,seq=genebank_db.seq)

        #处理前的序列  
        before_processed_seq_dict={
            'target_gene_seq':coordinate_2_seq( (target_gene_start,target_gene_end),seq=genebank_db.seq ),
            'target_gene_up_seq':coordinate_2_seq( (start,target_gene_start),seq=genebank_db.seq ),
            'target_gene_down_seq':coordinate_2_seq( (target_gene_end,end),seq=genebank_db.seq )     
        }

    elif tag == 1:                                                  #target_gene在零点处
        #处理gene目标
        target_gene1_coordinate = deal_coordinate(
                                                    'target_gene1',
                                                    target_gene1_start,
                                                    end,
                                                    opt=config.AMPLICONIC_GENE_TARGET_SEQ_LENGTH
                                                )
        target_gene2_coordinate = deal_coordinate(
                                                    'target_gene2',
                                                    start,
                                                    target_gene2_end,
                                                    opt=config.AMPLICONIC_GENE_TARGET_SEQ_LENGTH
                                                )
        marker_coordinate = deal_coordinate(
                                                'marker',
                                                marker_start,
                                                marker_end,
                                                opt=config.AMPLICONIC_MARKER_SEQ_LENGTH
                                        )
         #取序列
        target_gene_seq = coordinate_2_seq(target_gene1_coordinate,seq=genebank_db.seq) + coordinate_2_seq(target_gene2_coordinate,seq=genebank_db.seq)
        marker_seq = coordinate_2_seq(marker_coordinate,seq=genebank_db.seq)
        target_gene_up_seq = coordinate_2_seq( (marker_coordinate[1], target_gene1_coordinate[0]) ,seq=genebank_db.seq)
        target_gene_down_seq = coordinate_2_seq( (target_gene2_coordinate[1], marker_coordinate[0]) ,seq=genebank_db.seq)  
         

         #处理前的序列  
        before_processed_seq_dict={
            'target_gene_seq':coordinate_2_seq( (target_gene1_start, target_gene1_end) ,seq=genebank_db.seq) + coordinate_2_seq( (target_gene2_start, target_gene2_end) ,seq=genebank_db.seq),
            'target_gene_up_seq':coordinate_2_seq( (target_gene2_end, target_gene1_start) ,seq=genebank_db.seq),
            'target_gene_down_seq':'' 
        }   


    elif tag == 2:                                                  #marker在零点处
        #处理marker目标
        if marker1_end - marker1_start >= config.AMPLICONIC_MARKER_SEQ_LENGTH:
            marker_coordinate = deal_coordinate(
                                                'marker',
                                                marker1_start,
                                                marker1_end,
                                                opt=config.AMPLICONIC_MARKER_SEQ_LENGTH
                                        )
            #取marker序列
            marker_seq = coordinate_2_seq(marker_coordinate,seq=genebank_db.seq)
            target_gene_seq = coordinate_2_seq(target_gene_coordinate,seq=genebank_db.seq)
            target_gene_up_seq =  coordinate_2_seq( (marker_coordinate[1],end),seq=genebank_db.seq ) + coordinate_2_seq( (start,target_gene_coordinate[0]),seq=genebank_db.seq )
            target_gene_down_seq = coordinate_2_seq( (target_gene_coordinate[1], marker_coordinate[0]) ,seq=genebank_db.seq)
           
        else:
            marker1_coordinate = deal_coordinate(
                                                'marker',   
                                                marker1_start,
                                                end,
                                                opt=config.AMPLICONIC_MARKER_SEQ_LENGTH
                                        )

            marker2_coordinate = deal_coordinate(
                                                'marker',
                                                marker2_start,
                                                marker2_end,
                                                opt=config.AMPLICONIC_MARKER_SEQ_LENGTH-(marker1_end-marker1_start)
                                        ) 
            #取marker序列
            marker_seq = coordinate_2_seq(marker1_coordinate,seq=genebank_db.seq) + coordinate_2_seq(marker2_coordinate,seq=genebank_db.seq)
            target_gene_seq = coordinate_2_seq(target_gene_coordinate,seq=genebank_db.seq)
            target_gene_up_seq =  coordinate_2_seq( (marker2_coordinate[1], target_gene_coordinate[0]),seq=genebank_db.seq )
            target_gene_down_seq = coordinate_2_seq( (target_gene_coordinate[1], end),seq=genebank_db.seq ) + coordinate_2_seq( (start, marker1_coordinate[1]),seq=genebank_db.seq )

        #处理前的序列  
        before_processed_seq_dict={
            'target_gene_seq': coordinate_2_seq( (target_gene_start,target_gene_end),seq=genebank_db.seq ),
            'target_gene_up_seq': coordinate_2_seq( (marker2_end, target_gene_start),seq=genebank_db.seq ),
            'target_gene_down_seq': coordinate_2_seq( (target_gene_end,marker1_start),seq=genebank_db.seq )     
        }
        
    #处理后的序列
    after_processed_seq_dict = {
        'target_gene_seq':target_gene_seq,  
        'marker_seq':marker_seq,
        'target_gene_down_seq':target_gene_down_seq,
        'target_gene_up_seq':target_gene_up_seq
    }
   
     
    return before_processed_seq_dict, after_processed_seq_dict      


         