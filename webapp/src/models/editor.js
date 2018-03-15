/* eslint-disable */
// enable eslint again if you are using this file
import _ from 'lodash';
import store from '@/store';
export const getIndexOf = (text, itm) => {
  const index = itm ? text.lastIndexOf(itm) : text.length;
  return index;
};

export const getLengthOf = (itm) => {
  const index = itm ? itm.length : 1;
  return index;
};

export const makeFeedback = (pass, startIndex, index, end, msg, action) => ({
  pass,
  index: index + startIndex,
  length: end,
  msg,
  action,
});

export const InvalidRuleResponse = (startIndex, text) =>
  makeFeedback(
    false,
    startIndex,
    getIndexOf(text, text),
    getLengthOf(text),
    'Invalid Rule',
    ['color', 'red'],
  );
/*eslint-disable */
export const splitLine = (text) => text.split(/\s+/);
/*eslint-enable */
export const checkVersion = (text, version, startIndex) => {
  if (!text.toLowerCase().startsWith('v')) {
    return makeFeedback(false, startIndex, 0, 1, 'Invalid version rule', [
      'color',
      'red',
    ]);
  }
  const fields = splitLine(text);
  if (fields.length !== 2) {
    return makeFeedback(
      false,
      startIndex,
      1,
      text.length,
      'Invalid version rule length',
      ['color', 'red'],
    );
  }
  if (fields[1] !== String(version)) {
    return makeFeedback(
      false,
      startIndex,
      1,
      text.length,
      'script version does not match with parser version',
      ['color', 'red'],
    );
  }

  return makeFeedback(true, startIndex, 0, text.length, 'Valid version rule', [
    'color',
    'green',
  ]);
};
export const validatePlate = (text, existingPlates, startIndex) => {
  if (!text.replace(/ /g, '').match(/^P\d+$/)) {
    return makeFeedback(
      false,
      startIndex,
      0,
      text.length,
      'Invalid Plate Rule',
      ['color', 'red'],
    );
  }

  const plateNumber = text.match(/^P \d+$/g).join();

  if (existingPlates.indexOf(plateNumber.trim()) > -1) {
    return makeFeedback(
      false,
      startIndex,
      1,
      text.length,
      'Plate Already Exists',
      ['color', 'red'],
    );
  }

  store.commit('SET_CURRENT_PLATE_FROM_SCRIPT', text.replace(/ /g, ''));
  store.commit('SET_PARSED_PLATE', text.replace(/ /g, ''));
  return makeFeedback(true, startIndex, 0, text.length, 'Valid Plate Rule', [
    'color',
    'green',
  ]);
};
export const checkPlate = (currentPlate, lineStartIndex, text) => {
  if (!currentPlate) {
    return makeFeedback(
      false,
      lineStartIndex,
      0,
      text.length,
      'Please Specify a Plate',
      ['color', 'red'],
    );
  }
  return null;
};
export const checkFields = (lineStartIndex, text) => {
  const fields = splitLine(text);
  if (fields.length > 6) {
    return makeFeedback(
      false,
      lineStartIndex,
      0,
      text.length,
      'unexpected number of elements',
      ['color', 'red'],
    );
  }
  if (fields.length < 6) {
    return makeFeedback(
      true,
      lineStartIndex,
      0,
      text.length,
      'Rule Incomplete',
      ['color', 'orange'],
    );
  }

  return null;
};
export const checkAllocationReagent = (
  lineStartIndex,
  reagents,
  fields,
  text,
) => {
  if (fields[1] && reagents.indexOf(fields[1]) === -1) {
    const suggestions = reagents.filter((x) => x.indexOf(fields[1]) > -1);
    store.commit('SET_SUGGESTIONS', suggestions);
    return makeFeedback(
      false,
      lineStartIndex,
      getIndexOf(text, fields[1]),
      getLengthOf(fields[1]),
      'Not a recogonised reagent',
      ['color', 'red'],
    );
  }

  return null;
};
export const checkTransferReagent = (
  lineStartIndex,
  plates,
  currentPlate,
  fields,
  text,
) => {
  if (fields[1] && plates.indexOf(fields[1]) === -1) {
    return makeFeedback(
      false,
      lineStartIndex,
      getIndexOf(text, fields[1]),
      getLengthOf(fields[1]),
      'Not a recogonised plate',
      ['color', 'red'],
    );
  }
  if (fields[1] === currentPlate) {
    return makeFeedback(
      false,
      lineStartIndex,
      getIndexOf(text, fields[1]),
      getLengthOf(fields[1]),
      'Transfer Rule points to current plate',
      ['color', 'red'],
    );
  }
  return null;
};
export const checkColRange = (lineStartIndex, fields, text) => {
  if (
    fields[2] &&
    !(
      fields[2].match(/^\d+-\d+$/) ||
      fields[2].match(/^\d+$/) ||
      fields[2].match(/^(?!,)(,?[0-9]+)+$/)
    )
  ) {
    return makeFeedback(
      false,
      lineStartIndex,
      getIndexOf(text, fields[2]),
      getLengthOf(fields[2]),
      'Not a valid col range',
      ['color', 'red'],
    );
  }
  return null;
};
export const checkRowRange = (lineStartIndex, fields, text) => {
  if (
    fields[3] &&
    !(
      fields[3].match(/^[A-Z]-[A-Z]$/) ||
      fields[3].match(/^(?!,)(,?[A-Z])+$/) ||
      fields[3].match(/^[A-Z]$/)
    )
  ) {
    return makeFeedback(
      false,
      lineStartIndex,
      getIndexOf(text, fields[3]),
      getLengthOf(fields[3]),
      'Not a valid col range',
      ['color', 'red'],
    );
  }
  return null;
};
export const checkConcentration = (lineStartIndex, fields, text) => {
  if (fields[4] && !isFinite(fields[4])) {
    return makeFeedback(
      false,
      lineStartIndex,
      getIndexOf(text, fields[4]),
      getLengthOf(fields[4]),
      'Invalid number',
      ['color', 'red'],
    );
  }
  return null;
};
export const checkUnits = (lineStartIndex, units, fields, text) => {
  if (fields[5] && units.indexOf(fields[5]) === -1) {
    const suggestions = units.filter((x) => x.indexOf(fields[5]) > -1);
    store.commit('SET_SUGGESTIONS', suggestions);
    return makeFeedback(
      false,
      lineStartIndex,
      getIndexOf(text, fields[5]),
      getLengthOf(fields[5]),
      'Invalid units',
      ['color', 'red'],
    );
  }
  return null;
};
export const accumulateFeedBacks = (lineStartIndex, feedback, text) => {
  if (_.isEmpty(feedback.filter((x) => x))) {
    return makeFeedback(true, lineStartIndex, 0, text.length, 'Valid Rule', [
      'color',
      'green',
    ]);
  }
  return feedback;
};
export const validateRule = (
  text,
  reagents,
  units,
  existingPlates,
  lineStartIndex,
  currentPlate,
) => {
  const fields = splitLine(text);
  const ruleFeedBacks = [];
  ruleFeedBacks.push(checkPlate(currentPlate, lineStartIndex, text));
  ruleFeedBacks.push(checkFields(lineStartIndex, text));
  if (fields[0] === 'A') {
    ruleFeedBacks.push(
      checkAllocationReagent(lineStartIndex, reagents, fields, text),
    );
  } else if (fields[0] === 'T') {
    ruleFeedBacks.push(
      checkTransferReagent(
        lineStartIndex,
        existingPlates,
        currentPlate,
        fields,
        text,
      ),
    );
  } else {
    return InvalidRuleResponse(lineStartIndex, fields, text);
  }
  ruleFeedBacks.push(checkColRange(lineStartIndex, fields, text));
  ruleFeedBacks.push(checkRowRange(lineStartIndex, fields, text));
  ruleFeedBacks.push(checkConcentration(lineStartIndex, fields, text));
  ruleFeedBacks.push(checkUnits(lineStartIndex, units, fields, text));

  return accumulateFeedBacks(lineStartIndex, ruleFeedBacks, text);
};
export const validateComment = (text, startIndex) =>
  makeFeedback(true, startIndex, 0, text.length, 'valid comment', [
    'color',
    'blue',
  ]);
export const getFeedback = (line, args) => {
  const {
    startIndex,
    version,
    parsedPlates,
    reagents,
    units,
    currentPlate,
  } = args;

  let result;

  switch (true) {
    case line.startsWith('V'):
      result = checkVersion(line, version, startIndex);
      break;
    case line.startsWith('P'):
      result = validatePlate(line, parsedPlates, startIndex);
      break;
    case line[0] === 'A' || line[0] === 'T':
      result = validateRule(
        line,
        reagents,
        units,
        parsedPlates,
        startIndex,
        currentPlate,
      );
      break;
    case line.startsWith('#'):
      result = validateComment(line, startIndex);
      break;
    case _.isEmpty(line):
      //  do absolutely nothig just sit there
      break;
    default:
      result = InvalidRuleResponse(startIndex, line);
  }
  return result;
};

export const validateText = (text, args) => {
  let startIndex = 0;
  let feedBackCollector = [];
  const lines = text.split('\n');

  _.transform(lines, (acc, line) => {
    feedBackCollector = feedBackCollector
      .concat(getFeedback(line, { ...args, startIndex }))
      .filter((x) => x);

    if (!_.isEmpty(feedBackCollector.filter((x) => !x.pass))) {
      const pos = feedBackCollector.filter((x) => x.pass);
      const neg = feedBackCollector.filter((x) => !x.pass);
      store.commit('SET_VALID_OBJECTS', pos);
      store.commit('SET_INVALID_OBJECTS', neg);
      return false;
    }
    startIndex += line.length + 1;
    return true;
  });

  /*eslint-disable */
  feedBackCollector = feedBackCollector.filter((x) => x);
  const pos = feedBackCollector.filter((x) => x.pass);
  const neg = feedBackCollector.filter((x) => !x.pass);
  store.commit('SET_VALID_OBJECTS', pos);
  store.commit('SET_INVALID_OBJECTS', neg);

  // return feedBackCollector.filter((x) => x);
  /*eslint-enable */
};
