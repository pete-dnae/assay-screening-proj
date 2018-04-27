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
    pureAxios.get(url).then(
      ({ data }) => {
        const response = _.isEmpty(data) ? null : data;
        resolve(response);
      },
      (err) => {
        reject(err);
      },
    );
  });
const putRes = (url, data) =>
  pureAxios.put(url, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

const postRes = (url, data) => axios.post(url, data, {
  headers: {
    'Content-Type': 'application/json',
  },
});


export const getExperiment = experimentName => fetchRes(`api/experiments/${experimentName}/`);
export const getPlate = plateId => fetchRes(`api/plates/${plateId}/`);
export const getRuleScript = url => fetchResPure(url);
export const postRuleScript = data =>
  postRes('/api/rule-scripts/', data);
export const getExperimentList = () => fetchRes('api/experiments/');
export const putRuleSCript = ({ ruleScriptUrl, text }) => putRes(
           ruleScriptUrl,
           { text },
         );
export const getReagents = () => fetchRes('/api/reagents/');
export const getUnits = () => fetchRes('/api/units/');
export const postNewExperiment = data =>
  postRes('/api/experiments/', data);
export const getAvailableSuggestions = () => fetchRes('/api/allowed-names');
export const getExperimentImages = experimentName => fetchRes(`/api/experiment-images/${experimentName}`);
