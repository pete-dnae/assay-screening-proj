import _ from 'lodash';
export const splitLine = text => text.split(/\s+/);
export const makeFeedback = (pass, startIndex, index, end, msg) => ({
  pass,
  index: index + startIndex,
  length: end,
  msg,
});
export const checkVersion = (text, version, startIndex) => {
  if (!text.toLowerCase().startsWith('v')) {
    return makeFeedback(false, startIndex, 0, 1, 'Invalid version rule');
  }
  const fields = splitLine(text);
  if (fields.length !== 2) {
    return makeFeedback(
      false,
      startIndex,
      1,
      text.length,
      'Invalid version rule length',
    );
  }
  if (fields[1] != version) {
    return makeFeedback(
      false,
      startIndex,
      1,
      text.length,
      'script version does not match with parser version',
    );
  }

  return makeFeedback(true, startIndex, 0, text.length, 'Valid version rule');
};
export const validatePlate = (text, existingPlates, startIndex) => {
  if (!text.match(/^P\d+$/)) {
    return makeFeedback(
      false,
      startIndex,
      0,
      text.length,
      'Invalid Plate Rule',
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
    );
  }
  return makeFeedback(true, startIndex, 0, text.length, 'Valid Plate Rule');
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
    );
  }
  if (fields[0] === 'A') {
    if (!fields[1] || reagents.indexOf(fields[1]) === -1) {
      return makeFeedback(
        false,
        lineStartIndex,
        text.indexOf(fields[1]),
        fields[1] ? fields[1].length : 0,
        'Not a recogonised reagent',
      );
    }
  } else if (fields[0] === 'T') {
    if (!fields[1] || existingPlates.indexOf(fields[1]) === -1) {
      return makeFeedback(
        false,
        lineStartIndex,
        text.indexOf(fields[1]),
        fields[1] ? fields[1].length : 0,
        'Not a recogonised plate',
      );
    }
  }

  if (
    !fields[2] ||
    !(
      fields[2].match(/^\d+-\d+$/) ||
      fields[2].match(/^\d+$/) ||
      fields[2].match(/^(?!,)(,?[0-9]+)+$/)
    )
  ) {
    return makeFeedback(
      false,
      lineStartIndex,
      text.indexOf(fields[2]),
      fields[2] ? fields[2].length : 0,
      'Not a valid col range',
    );
  }

  if (
    !fields[3] ||
    !(
      fields[3].match(/^[A-Z]-[A-Z]$/) ||
      fields[3].match(/^(?!,)(,?[A-Z])+$/) ||
      fields[3].match(/^[A-Z]$/)
    )
  ) {
    return makeFeedback(
      false,
      lineStartIndex,
      text.indexOf(fields[3]),
      fields[3] ? fields[3].length : 0,
      'Not a valid col range',
    );
  }

  if (!fields[4] || !isFinite(fields[4])) {
    return makeFeedback(
      false,
      lineStartIndex,
      text.indexOf(fields[4]),
      fields[4] ? fields[4].length : 0,
      'Invalid number',
    );
  }

  if (!fields[5] || units.indexOf(fields[5]) === -1) {
    return makeFeedback(
      false,
      lineStartIndex,
      text.indexOf(fields[5]),
      fields[5] ? fields[5].length : 0,
      'Invalid units',
    );
  }
  return makeFeedback(true, lineStartIndex, 0, text.length, 'Valid rule');
};
export const validateComment = (text, startIndex) =>
  makeFeedback(true, startIndex, startIndex, text.length, 'valid comment');
