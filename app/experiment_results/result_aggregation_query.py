GroupByIDASSAY = """
select 
well_aggregation.experiment_id,
well_aggregation.qpcr_plate_id,
string_agg(well_aggregation.qpcr_well, ',' order by well_aggregation.qpcr_well) as wells,
well_aggregation.assays,
ARRAY_AGG(DISTINCT well_aggregation.transfered_assays) as transfered_assays,
ARRAY_AGG( DISTINCT well_aggregation.templates) as templates,
ARRAY_AGG(DISTINCT well_aggregation.transfered_templates) as transfered_templates,
ARRAY_AGG( DISTINCT well_aggregation.reagent_group) as reagent_group,
ARRAY_AGG(DISTINCT well_aggregation.transfered_reagent_group) as transfered_reagent_group,
ARRAY_AGG( DISTINCT well_aggregation.reagent_group_entities) as reagent_group_entities,
ARRAY_AGG(DISTINCT well_aggregation.transfered_reagent_group_entities) as transfered_reagent_group_entities
from 
(select 
merged.experiment_id,
merged.qpcr_plate_id,
merged.qpcr_well, 
string_agg(merged.assay, ',' order by merged.assay) as assays,
string_agg(merged.transfered_assay, ',' order by merged.transfered_assay) as transfered_assays,
string_agg(merged.templates, ',' order by merged.templates) as templates,
string_agg(merged.transfered_templates, ',' order by merged.transfered_templates) as transfered_templates,
merged.reagent_group,
merged.transfered_reagent_group,
 merged.reagent_group_entities,
merged.transfered_reagent_group_entities
from 
(select  
qpcr.experiment_id,
qpcr.qpcr_plate_id,
qpcr.qpcr_well,
(case when reagents.category='assay' and reagents.reagentTransfer = false then reagents.reagent end) as assay,
(case when reagents.category='assay' and reagents.reagentTransfer = true then reagents.reagent end) as transfered_assay,
(case when reagents.category='template' and reagents.reagentTransfer = false then reagents.reagent end) as templates,
(case when reagents.category='template' and reagents.reagentTransfer = true then reagents.reagent end) as transfered_templates,
 (case when  reagents.reagentGroupTransfer = false then reagents.reagentGroup end) as reagent_group,
 (case when  reagents.reagentGroupTransfer = true then reagents.reagentGroup end) as transfered_reagent_group,
  (case when  reagents.reagentGroupTransfer = false then reagents.reagentGroupEntities end) as reagent_group_entities,
 (case when  reagents.reagentGroupTransfer = true then reagents.reagentGroupEntities end) as transfered_reagent_group_entities
from app_qpcrresultsmodel as qpcr Inner Join (
(select 
 re.well_id,
 re.reagent_id as reagent,
 re.category_id as category,
 re.transfer as reagentTransfer,  
 rgp.reagentGroup,
 rgp.reagents as reagentGroupEntities,
 rgp.transfer as reagentGroupTransfer
 from
(select 
rwl.well_id,
rwl.reagent_id,
r.category_id,
rwl.transfer
from app_reagentwelllookupmodel as rwl
inner join app_reagentmodel as r on rwl.reagent_id = r.name) as re
left join
(select 
rgl.well_id,
rgl.transfer,
rgl.reagent_group_id as reagentGroup, 
string_agg(rgd.reagent_id, ',' order by rgd.reagent_id) as reagents
from app_reagentgroupwelllookupmodel  as rgl
inner join app_reagentgroupdetailsmodel
as rgd on rgl.reagent_group_id = rgd.reagent_group_id 
group by rgl.reagent_group_id,rgl.well_id,rgl.transfer,rgl.reagent_group_id) as rgp
on rgp.well_id=re.well_id)
) as reagents 
on qpcr.id = reagents.well_id) as merged
group by merged.experiment_id,
merged.qpcr_plate_id,
merged.qpcr_well,
merged.reagent_group,
merged.transfered_reagent_group,
 merged.reagent_group_entities,
merged.transfered_reagent_group_entities) as well_aggregation
group by well_aggregation.experiment_id,
well_aggregation.qpcr_plate_id,
well_aggregation.assays
"""