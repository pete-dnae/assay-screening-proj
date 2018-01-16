import axios from 'axios';
import _ from 'lodash';


const fetchRes = url =>
  axios.get(url).then(({
    data,
  }) => {
    const response = _.isEmpty(data) ? null : data;
    return response;
  });

const postRes = (url, data) => {
  debugger;
  return axios.post(
  url,
  data, {
    headers: {
      'Content-Type': 'application/json',
    },
  },
);
};

export const getExperiment = expNo => fetchRes(`api/experiments/${expNo}/`);

export const updateAllocationRules = (url, data) => postRes(url, data);
