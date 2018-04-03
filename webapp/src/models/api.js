import axios from 'axios';
import _ from 'lodash';

const pureAxios = axios.create();

const fetchRes = url =>
  new Promise((resolve, reject) => {
    axios.get(url).then(
      ({ data }) => {
        const response = _.isEmpty(data) ? null : data;
        resolve(response);
      },
      (err) => {
        reject(err);
      },
    );
  });

const fetchResPure = url =>
  new Promise((resolve, reject) => {
    pureAxios.get(url).then(({ data }) => {
      const response = _.isEmpty(data) ? null : data;
      resolve(response);
    }, (err) => {
      reject(err);
    });
  });
const putRes = (url, data) =>
  axios.put(url, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

export const getExperiment = expNo => fetchRes(`api/experiments/${expNo}/`);
export const getPlate = plateId => fetchRes(`api/plates/${plateId}/`);
// TODO : check with pete if he can deliver the rulescript uniqueid alone
export const getRuleScript = url => fetchResPure(url);

export const getExperimentList = () => fetchRes('api/experiments/');
export const putRuleSCript = ({ ruleScriptNo, text }) =>
  putRes(`api/rule-scripts/${ruleScriptNo}/`, { text });
export const getReagents = () => fetchRes('/api/reagents/');
export const getUnits = () => fetchRes('/api/units/');
