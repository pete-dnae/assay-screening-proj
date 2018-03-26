import axios from 'axios';
import _ from 'lodash';
//eslint-disable-next-line
const fetchRes = (url) =>
  axios.get(url).then(({ data }) => {
    const response = _.isEmpty(data) ? null : data;
    return response;
  });

// const postRes = (url, data) =>
//   axios.post(url, data, {
//     headers: {
//       'Content-Type': 'application/json',
//     },
//   });

const putRes = (url, data) =>
  axios.put(url, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });


export const getExperiment = expNo => fetchRes(`api/experiments/${expNo}/`);
export const getPlate = plateId => fetchRes(`api/plates/${plateId}/`);
// TODO : check with pete if he can deliver the rulescript uniqueid alone
export const getRuleScript = () => fetchRes('api/rule-scripts/1/');

export const getExperimentList = () => fetchRes('api/experiments/');
export const postRuleSCript = ({ ruleScriptNo, text }) =>
  putRes(`api/rule-scripts/${ruleScriptNo}/`, { text });
export const getReagents = () => fetchRes('/api/reagents/');
export const getUnits = () => fetchRes('/api/units/');
