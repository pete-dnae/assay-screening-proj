import store from '@/store';
import _ from 'lodash';

export const postRuleScript = (text, ruleScriptNo, callBack) => {
  store
    .dispatch('saveToDb', {
      text,
      ruleScriptNo,
    })
    .then(() => callBack());
};

export const getMaxRowCol = (lnums) => {
  const allCells = _.reduce(
    lnums,
    (acc, x) => {
      Object.assign(acc, acc.concat(x));
      return acc;
    },
    [],
  );

  return [
    // extending boundary by one to display table boundaries
    allCells.sort((a, b) => b[1] - a[1])[0][1],
    allCells.sort((a, b) => b[0] - a[0])[0][0],
  ];
};

export const splitLine = (text) => {
  const re = /\S+/g;
  const fields = [];
  let match;
  //eslint-disable-next-line
  while ((match = re.exec(text))) {
    fields.push(match);
  }
  return fields;
};

export const getChildIndex = (child) => {
  const parent = child.parentNode;
  const children = parent.children;
  let plateName = null;
  let lineNumber = 0;
  for (; lineNumber <= children.length - 1; lineNumber += 1) {
    const innerText = children[lineNumber].innerText;

    if (child === children[lineNumber]) {
      break;
    }

    if (innerText.startsWith('P')) {
      [, plateName] = innerText.split(/\s+/g);
    }
  }
  return { lineNumber, plateName };
};

export const startEndOfLine = (lineNumber, text) => [
  text.split('\n', lineNumber).join('\n').length,
  text.split('\n', lineNumber + 1).join('\n').length,
];
//eslint-disable-next-line
export const removeAdditionalNewLine = currentText => currentText.slice(0, -1);

export const getCurrentLineFields = (currentText, cursorPosition) => {
  const currentLineStart = removeAdditionalNewLine(currentText)
    .substr(0, cursorPosition)
    .lastIndexOf('\n');

  const currentLine = currentText.substr(
    currentLineStart === -1 ? 0 : currentLineStart,
    cursorPosition,
  );
  return splitLine(currentLine);
};

export const hesitationTimer = _.debounce(postRuleScript, 500);

export const fieldIndexRange = (lineStart, field) => {
  const startIndex = lineStart + field.index;
  const length = field[0].length;
  return { startIndex, length };
};
export const validateVersion = (startIndex, fields, text) => {
  let err = { startIndex, length: text.length, action: [{ color: 'red' }] };

  if (!fields[1]) {
    err = {
      ...err,
      err: 'No version number',
    };
    throw err;
  }
  //eslint-disable-next-line
  if (fields[1][0] != store.getters.getVersion) {
    err = {
      ...err,
      err: `Parser version mismatch expected ${store.getters.getVersion} `,
    };
    throw err;
  }
  store.commit('SET_VERSION_VERIFIED', true);
};

export const validateRowRange = (startIndex, fields) => {
  if (
    fields[2] &&
    !(
      fields[2][0].match(/^\d+-\d+$/) ||
      fields[2][0].match(/^\d+$/) ||
      fields[2][0].match(/^(?!,)(,?[0-9]+)+$/)
    )
  ) {
    const err = {
      ...fieldIndexRange(startIndex, fields[2]),
      err: 'Not a valid row range',
      action: [{ color: 'red' }],
    };
    throw err;
  }
};
export const validateColRange = (startIndex, fields) => {
  if (
    fields[3] &&
    !(
      fields[3][0].match(/^[A-Z]-[A-Z]$/) ||
      fields[3][0].match(/^(?!,)(,?[A-Z])+$/) ||
      fields[3][0].match(/^[A-Z]$/)
    )
  ) {
    const err = {
      ...fieldIndexRange(startIndex, fields[3]),
      err: 'Not a valid col range',
      action: [{ color: 'red' }],
    };
    throw err;
  }
};
export const validateConcentration = (startIndex, fields) => {
  if (fields[4] && !isFinite(fields[4][0])) {
    const err = {
      ...fieldIndexRange(startIndex, fields[4]),
      err: 'Not a valid concentration',
      action: [{ color: 'red' }],
    };
    throw err;
  }
};
export const validateFields = (startIndex, fields, text) => {
  if (fields.length !== 6) {
    const err = {
      startIndex,
      length: text.length,
      err: `There should be 6 fields but found ${fields.length} : ${fields.join(
        ',',
      )}`,
      action: [{ color: 'orange' }],
    };
    throw err;
  }
};

export const validateUnits = (startIndex, fields) => {
  if (fields[5] && store.getters.getUnits.indexOf(fields[5][0]) === -1) {
    const err = {
      ...fieldIndexRange(startIndex, fields[5]),
      err: 'Not a valid unit',
      action: [{ color: 'red' }],
    };
    throw err;
  }
};
export const validateRule = (startIndex, fields, text) => {
  if (_.isEmpty(store.getters.getCurrentPlate)) {
    const err = {
      startIndex,
      length: text.length,
      action: [{ color: 'red' }],
      err: 'No current Plate',
    };
    throw err;
  }
  if (fields[0] && fields[0][0] === 'A') {
    if (fields[1]) {
      let err = {
        ...fieldIndexRange(startIndex, fields[1]),
        action: [{ color: 'red' }],
      };
      if (store.getters.getReagents.indexOf(fields[1][0]) === -1) {
        const suggestions = store.getters.getReagents.filter(
          //eslint-disable-next-line
          x => x.indexOf(fields[1][0]) > -1
        );

        store.commit('SET_SUGGESTIONS', suggestions);
        if (_.isEmpty(suggestions)) {
          err = { ...err, err: 'Reagent name doesnt match' };
          throw err;
        } else if (suggestions.length > 1) {
          err = {
            ...err,
            err: `There are currently ${suggestions.length} matches `,
          };

          throw err;
        }
      }
    }
    validateColRange(startIndex, fields);
    validateRowRange(startIndex, fields);
    validateConcentration(startIndex, fields);
    validateUnits(startIndex, fields);
    validateFields(startIndex, fields, text);
  } else if (fields[0] && fields[0][0] === 'T') {
    if (fields[1]) {
      let err = {
        ...fieldIndexRange(startIndex, fields[1]),
        action: [{ color: 'red' }],
      };
      if (store.getters.getParsedPlates.indexOf(fields[1][0]) === -1) {
        err = { ...err, err: 'Not a recogonised plate' };
        throw err;
      }
      if (store.getters.getCurrentPlate === fields[1][0]) {
        err = { ...err, err: 'Cannot transfer from current plate' };
        throw err;
      }
    }
    validateColRange(startIndex, fields);
    validateRowRange(startIndex, fields);
    validateConcentration(startIndex, fields);
    validateUnits(startIndex, fields);
    validateFields(startIndex, fields, text);
  } else {
    const err = {
      startIndex,
      length: text.length,
      err: 'first field not present',
    };
    throw err;
  }
};
export const validatePlate = (startIndex, fields, text) => {
  if (!store.getters.getVersionVerified) {
    const err = {
      startIndex,
      length: text.length,
      action: [{ color: 'red' }],
      err: 'Version not verified',
    };
    throw err;
  }
  let err = { startIndex, length: text.length, action: [{ color: 'red' }] };
  if (fields.length !== 2) {
    err = {
      ...err,
      err: `Unexpected number of fields (${fields.join(',')}) in plate rule`,
    };
    throw err;
  }
  if (fields[1] && store.getters.getParsedPlates.indexOf(fields[1][0]) > -1) {
    err = {
      ...err,
      err: `plate name ${fields[2]} is already parsed`,
    };
    throw err;
  }
  store.commit('SET_CURRENT_PLATE_FROM_SCRIPT', fields[1][0]);
  store.commit('SET_PARSED_PLATE', fields[1][0]);
};
export const handleRuleCases = (line, startIndex) => {
  // const { startIndex, version, reagents, units } = args;

  const fields = splitLine(line);
  const err = {
    startIndex,
    length: line.length,
    err: 'Not a valid rule / comment , what are you ?',
    action: [{ color: 'red' }],
  };

  switch (true) {
    case _.isEmpty(line):
      //  do absolutely nothig just sit there
      break;
    case fields[0][0] === 'V':
      validateVersion(startIndex, fields, line);
      break;
    case fields[0][0] === 'P':
      validatePlate(startIndex, fields, line);
      break;
    case fields[0][0] === 'A' || fields[0][0] === 'T':
      validateRule(startIndex, fields, line);
      break;
    case fields[0][0] === '#':
      break;
    default:
      throw err;
  }
};

export const validateText = (text) => {
  let startIndex = 0;

  store.commit('CLEAR_PARSED_PLATE');
  const lines = text.split('\n');
  try {
    lines.forEach((line) => {
      handleRuleCases(line, startIndex);

      startIndex += line.length + 1;
    });
    store.commit('SET_VALID_SCRIPT', text);
  } catch (e) {
    store.commit('LOG_ERROR', e);
    store.commit('SET_VALID_SCRIPT', text.substr(0, startIndex));
  }
};
