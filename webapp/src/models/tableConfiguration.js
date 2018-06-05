export const MASTER_HEADERS = {
  'qPCR Plate': { title: 'qPCR Plate', array: false, round: false },
  'qPCR Well': { title: 'qPCR Well', array: false, round: false },
  'LC Plate': { title: 'LC Plate', array: false, round: false },
  'LC Well': { title: 'LC Well', array: false, round: false },
  'PA Assay Name': { title: 'PA Assay Name.', array: true, round: false },
  'PA Template Conc.': { title: 'PA Template Conc.', array: true, round: true },
  'PA Human Conc.': { title: 'PA Human Conc.', array: true, round: true },
  'ID Template Conc.': { title: 'ID Template Conc.', array: true, round: true },
  'ID Human Conc.': { title: 'ID Human Conc.', array: true, round: true },
  Ct: { title: 'Ct', array: false, round: true },
  '∆NTC Ct': { title: '∆NTC Ct', array: false, round: true },
  'Ct Call': { title: 'Ct Call', array: false, round: false },
  Tm1: { title: 'Tm1', array: false, round: true },
  Tm2: { title: 'Tm2', array: false, round: true },
  Tm3: { title: 'Tm3', array: false, round: true },
  Tm4: { title: 'Tm4', array: false, round: true },
  'Tm Specif': { title: 'Tm Specif', array: false, round: false },
  'Tm NS': { title: 'Tm NS', array: false, round: false },
  'Tm PD': { title: 'Tm PD', array: false, round: false },
  'Specif ng/ul': { title: 'Specif ng/ul', array: false, round: true },
  'NS ng/ul': { title: 'NS ng/ul', array: false, round: true },
  'PD ng/ul': { title: 'PD ng/ul', array: false, round: true },
};

export const SUMMARY_HEADERS = {
  'qPCR Plate': { title: 'qPCR Plate', array: false, round: false },
  'LC Plate': { title: 'LC Plate', array: false, round: false },
  'ID Assay Name': { title: 'ID Assay Name', array: true, round: false },
  'ID Assay Conc.': { title: 'ID Assay Conc.', array: true, round: false },
  'ID Template Name': { title: 'ID Template Name', array: true, round: false },
  'ID Template Conc.': {
    title: 'ID Template Conc.',
    array: true,
    round: false,
  },
  'ID Human Name': { title: 'ID Human Name', array: true, round: false },
  'ID Human Conc.': { title: 'ID Human Conc.', array: true, round: false },
  Reps: { title: 'qPCR Plate', array: false, round: false },
  '#Ct Pos': { title: '#Ct Pos', array: false, round: false },
  '#Tm Specif': { title: '#Tm Specif', array: false, round: false },
  '#Tm NS': { title: '#Tm NS', array: false, round: false },
  '#Tm PD': { title: '#Tm PD', array: false, round: false },
  'Min Ct': { title: 'Min Ct', array: false, round: true },
  'Mean Ct': { title: 'Mean Ct', array: false, round: true },
  'Max Ct': { title: 'Max Ct', array: false, round: true },
  'Mean ∆NTC Ct': { title: 'Mean ∆NTC Ct', array: false, round: true },
  'Min Tm1': { title: 'Min Tm1', array: false, round: true },
  'Mean Tm1': { title: 'Mean Tm1', array: false, round: true },
  'Max Tm1': { title: 'Max Tm1', array: false, round: true },
  'Mean Specif ng/ul': {
    title: 'Mean Specif ng/ul',
    array: false,
    round: true,
  },
  'Mean NS ng/ul': { title: 'Mean NS ng/ul', array: false, round: true },
  'Mean PD ng/ul': { title: 'Mean PD ng/ul', array: false, round: true },
};

export const SUMMARY_COLOR_CONFIG = ['Ct Call', 'Tm NS', 'Tm PD', 'Tm Specif'];

export const RESULTS_SUMMARY_HEADERS = {
  experiment_id: { title: 'Experiment', array: false },
  qpcr_plate_id: { title: 'QPCR Plate', array: false },
  assays: { title: 'Assays', array: false },
  transfered_assays: { title: 'Transfered Assays', array: true },
  templates: { title: 'Templates', array: true },
  transfered_templates: { title: 'Transfered Templates', array: true },
  reagent_group: { title: 'Reagent Group', array: true },
  transfered_reagent_group: { title: 'Transfered Reagent Group', array: true },
  //   reagent_group_entities: { title: 'Reagent Group Entities', array: true },
  //   transfered_reagent_group_entities:
//   { title: 'Transfered Reagent Group Entities', array: true },
};
export const RESULTS_COLOR_CONFIG = [];