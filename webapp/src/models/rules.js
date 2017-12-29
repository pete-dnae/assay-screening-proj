import _ from 'lodash';

export const isConcentrationValid = value => !_.isEmpty(value) && value.split(',').length == 3;
