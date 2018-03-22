import axios from 'axios';
import _ from 'lodash';

const fetchRes = (url) =>
  axios.get(url).then(({ data }) => {
    const response = _.isEmpty(data) ? null : data;
    return response;
  });

const putRes = (url, data) =>
  axios.put(url, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

const postRes = (url, data) =>
  axios.post(url, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

const patchRes = (url, data) =>
  axios.patch(url, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
/*eslint-disable */
export const getExperiment = (expNo) => fetchRes(`api/experiments/${expNo}/`);
export const getPlate = (plateId) => fetchRes(`api/plates/${plateId}/`);
export const getRuleScript = (url) => fetchRes(`api/rule-scripts/1/`);
/*eslint-enable */
export const getExperimentList = () => fetchRes('api/experiments/');
export const postRuleSCript = ({ ruleScriptNo, text }) =>
  postRes(`api/rule-scripts/${ruleScriptNo}/`, { text });
