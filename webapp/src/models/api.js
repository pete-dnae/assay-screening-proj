import axios from 'axios';
import _ from 'lodash';

const fetchRes = url =>
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

export const getExperiment = expNo => fetchRes(`api/experiments/${expNo}/`);

export const updateAllocationRules = (url, data) => putRes(url, data);
export const addAllocationRule = (url, data) => putRes(url, data);
export const updateRule = (url, data) => putRes(url, data);
export const getPlate = plateId => fetchRes(`api/plates/${plateId}/`);
