# Attempt to isolate the normalised logical INPUT entities in the experiment
# defined in A81_E131.xls

-------------------------------------------------------------------------------
MIX RELATED
-------------------------------------------------------------------------------

Concentration
    // Collection of parameters that defines a concentration.
    // e.g. stock = 3.3, final = 1.0, units = cp/ul
    Stock
    Final
    Units (from X, uM, ng/ul, cp/ul, mM, mg/ml etc.)

Concrete reagents
    // Explicit, non-derived reagent.
    // e.g. DNA free Water, Titatium PCR Buffer, KCl etc
    Name
    Lot
    Concentration

BufferMix
    // One table specialised to buffermix
    // e.g PA BufferMix
    Concrete reagents
    Volume
    Final volume

Mixed reagents
    // Cross reference to buffer mix.
    // E.g. PA BufferMix
    Name / ie cross reference
    Concentration

Placeholder reagents (e.g. Primers / Template)
    // Reagent speicified by role only no specifics.
    // E.g. primer or template
    Type from Primer|Template|gDNA
    Concentration

MasterMix
    // One table specialised as buffermix
    // e.g. PA MasterMix
    Concrete reagents
    Mixed reagents
    Placeholder reagents
    Final volume

Buffer + Master Mix
    // Pair of related tables
    // (e.g. PA BufferMix + PA MasterMix)
    Type from PA|ID
    One BufferMix
    One MasterMix

-------------------------------------------------------------------------------
PRIMER RELATED
-------------------------------------------------------------------------------
Interpretation of primer names used in excel
    Consider: Ec_uidA_6.x_Eco63_Eco60
    Ec is taxon eg Ecoli
    uidA is gene
    6.x is oli set always number.x or x.number
    Eco63 is fwd primer 
    Eco60 is rev primer

Gene
    Just a name, e.g. UidA

Primer
    Oligo code e.g. Eco66
    Full name e.g. Ecol_UidA_1_157_23_IDf
    Sequence, e.g. TTGAA....
    Role fwd/rev
    Organism that targets
    Gene that targets


Primer Pair
    // E.g.  nomenclature Ec_uidA_6.x_Eco63_Eco60
    forward primer
    reverse primer
    good for preamp bool
    good for ID bool

    NB we also need to understand what 1.x or x.1 or 6.x means - ignoring for
    now.

PA Primers
    // List of PrimerPair(s)
    list of pairs

ID Primers
    // List of PrimerPair(s)
    list of pairs

Primer Pool not needed

Primer Stock plates and piro plate
    // Confused

Primer Kit
    // Assembly of everything above
    Fwd Primer Conc
    Rev Primer Conc
    PA Primers
    ID Primers
    Primer Stock plates and piro plate

-------------------------------------------------------------------------------
ORGANISM RELATED
-------------------------------------------------------------------------------

Organism
    // E.g.Enterococcus faecalis 
    Name
    Abbr (e.g. Eco)

ARG
    // E.g. vanB
    Name

Strain // E.g. ATCC BAA-1705 
    Name
    Organism
    ARG
    Genome Size // e.g. 5300000


-------------------------------------------------------------------------------
CYCLING RELATED
-------------------------------------------------------------------------------

CyclingPattern
    // Times, temperatures, counts
    Regime name // eg suitable for fibble
    Activation time
    Activation temp
    Number of cycles
    Denat temp
    Denat time
    Anneal temp
    Anneal time
    Extend temp
    Extend time

// Omiting this for now - probably wants to go into experiment as first class
// attributes.
Experiment Cycling
    // A seperate cycling regime for PA vs ID
    PA Cycling Regime
    ID Cycling Regime

-------------------------------------------------------------------------------
PLATE PLANNING / ALLOCATION RELATED
-------------------------------------------------------------------------------

// This is about trying to describe the allocation of things to chambers by
// describing patterns, or recipes, instead of actual allocations. Let the
// scientist think about the scheme reasoning and intent and have the machine do
// do the actual allocation based on those rules.

// Consider for one of the plates only to start with.

Column repeats = 4

# 4 attributes, Repeated every 4 columns

Template Strain Allocation = {Eco, EfsVanB, EfsVanB, Kok} repeated

ID Primers
    = {Ec_uidA_x.2_Eco64_Eco66, Efs_cpn60_x.1_Efs03_Efs02, 4 off}  repeated

# 3 attributes expanded 4 times each 
    I.e. {5,5,50} expanded = {5,5,5,5, 5,5,5,5, 50,50,50,50} 

Template copies

    Rows A,B = {0,0,0} expanded 
    Rows C,D = {5,5,50} expanded 
    Rows E,F = {5,5,500} expanded
    Rows G,H = {5,5,5000} expanded

HgDNA
    Rows A,B,C,D,E = {0,0,0} expanded 
    Rows F,G,H = {3000,3000,0} expanded

Dilution Factor = {30,30,0} expanded

# Custom
PA Primers
    
    First 4 columns  = Pool
    Next 4 columns = {Ec_uidA_6.x_Eco63_Eco60, Efs_cpn60_1.x_Efs04_Efs01, 4 off)
    Next 4 Columns = None





-------------------------------------------------------------------------------
Todo
-------------------------------------------------------------------------------
Wells n rows / columns
Number of plates
layout rules for each plate in experiment
Experiment as a whole with meta

