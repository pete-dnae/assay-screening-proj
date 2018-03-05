import _ from 'lodash';
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
export const splitLine = (text) => text.split(/\s+/);

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
  if (fields[1] != version) {
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
  if (!text.match(/^P\d+$/)) {
    return makeFeedback(
      false,
      startIndex,
      0,
      text.length,
      'Invalid Plate Rule',
      ['color', 'red'],
    );
  }

  const plateNumber = text.match(/\d+$/g).join();
  if (existingPlates.indexOf(plateNumber) > -1) {
    return makeFeedback(
      false,
      startIndex,
      1,
      text.length,
      'Plate Already Exists',
      ['color', 'red'],
    );
  }
  return makeFeedback(true, startIndex, 0, text.length, 'Valid Plate Rule', [
    'color',
    'green',
  ]);
};

export const validateRule = (
  text,
  reagents,
  units,
  existingPlates,
  lineStartIndex,
) => {
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
  if (fields[0] === 'A') {
    if (fields[1] && reagents.indexOf(fields[1]) === -1) {
      return makeFeedback(
        false,
        lineStartIndex,
        getIndexOf(text, fields[1]),
        getLengthOf(fields[1]),
        'Not a recogonised reagent',
        ['color', 'red'],
      );
    }
  } else if (fields[0] === 'T') {
    if (fields[1] && existingPlates.indexOf(fields[1]) === -1) {
      return makeFeedback(
        false,
        lineStartIndex,
        getIndexOf(text, fields[1]),
        getLengthOf(fields[1]),
        'Not a recogonised plate',
        ['color', 'red'],
      );
    }
  }

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

  if (fields[5] && units.indexOf(fields[5]) === -1) {
    return makeFeedback(
      false,
      lineStartIndex,
      getIndexOf(text, fields[5]),
      getLengthOf(fields[5]),
      'Invalid units',
      ['color', 'red'],
    );
  }
  return makeFeedback(true, lineStartIndex, 0, text.length, 'Valid rule', [
    'color',
    'green',
  ]);
};
export const validateComment = (text, startIndex) =>
  makeFeedback(true, startIndex, 0, text.length, 'valid comment', [
    'color',
    'blue',
  ]);
export const getFeedback = (line, args) => {
  const { lineNum, startIndex, version, parsedPlates, reagents, units } = args;
  let result;
  switch (true) {
    case lineNum === 1:
      result = checkVersion(line, version, startIndex);
      break;
    case line.startsWith('P'):
      result = validatePlate(line, parsedPlates, startIndex);
      break;
    case line.startsWith('A') || line.startsWith('T'):
      result = validateRule(line, reagents, units, parsedPlates, startIndex);
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
  const feedBackCollector = [];
  const lines = text.split('\n');

  lines.forEach((line, i) => {
    const lineNum = i + 1;
    feedBackCollector.push(getFeedback(line, { ...args, lineNum, startIndex }));
    startIndex += line.length + 1;
  });
  return feedBackCollector.filter((x) => x);
};
