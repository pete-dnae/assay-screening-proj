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

const postRes = (url, data) =>
  axios.post(url, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

const fetchResWithParam = (url, params) =>
  new Promise((resolve, reject) => {
    axios.get(url, { params }).then(
      ({ data }) => {
        const response = _.isEmpty(data) ? null : data;
        resolve(response);
      },
      (err) => {
        reject(err);
      },
    );
  });

const deleteRes = (url, data) =>
  axios.delete(
    url,
    { data },
    {
      headers: {
        'Content-Type': 'application/json',
      },
    },
  );

export const getExperiment = experimentName =>
  fetchRes(`api/experiments/${experimentName}/`);
export const getPlate = plateId => fetchRes(`api/plates/${plateId}/`);
export const getRuleScript = url => fetchResPure(url);
export const postRuleScript = data => postRes('/api/rule-scripts/', data);
export const getExperimentList = () => fetchRes('api/experiments/');
export const putRuleSCript = ({ ruleScriptUrl, text }) =>
  putRes(ruleScriptUrl, { text });
export const getReagents = () => fetchRes('/api/reagents/');
export const getUnits = () => fetchRes('/api/units/');
export const postNewExperiment = data => postRes('/api/experiments/', data);
export const getAvailableSuggestions = () => fetchRes('/api/allowed-names');
export const getExperimentImages = experimentName =>
  fetchRes(`/api/experiment-images/${experimentName}`);
export const getAvailableReagentGroups = () =>
  fetchRes('/api/reagent-groups/');
export const getSelectedReagentGroup = reagentGroupName =>
  fetchResWithParam(`/api/reagent-groups/${reagentGroupName}/`);
export const postReagentGroup = reagentGroup =>
  postRes('/api/reagent-groups/', reagentGroup);
export const deleteReagentGroup = reagentGroupName =>
  deleteRes(`/api/reagent-groups/${reagentGroupName}/`);
export const addReagent = data => postRes('/api/reagents/', data);
export const removeReagent = reagentName =>
  deleteRes(`/api/reagents/${reagentName}/`);
export const editReagent = ({ data, reagentName }) =>
  putRes(`/api/reagents/${reagentName}/`, data);
export const getReagentCategories = () => fetchRes('/api/reagent-categories/');
export const getWellResultSummary = () => fetchRes('/api/well-aggregate/');
export const getWellSummary = ({ wellArray, experimentId, qpcrPlateId }) =>
  fetchRes(
    `/api/well-results/?expt=${experimentId}&plate_id=${qpcrPlateId}&wells=${wellArray}`,
  );
