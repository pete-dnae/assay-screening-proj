export const splitLine = (text) => text.split(/\s+/);

export const parseVersion = (args, fields, text) => {
  const { startIndex, version } = args;
  if (fields[1] !== version) {
    const err = {
      startIndex,
      endIndex: text.length,
      action: [{ color: 'red' }],
      err: `Parser version mismatch expected ${version} `,
    };
    throw err;
  }
};
export const parseRule = (args, fields, text) => {
  const { startIndex, reagents, units } = args;
  let err ={
    startIndex,
    action: [{ color: 'red' }],
  }
  if (fields[0] === 'A') {
  } else if (fields[0]==='T') {
  }else{
    throw
  }
};
export const doYourThing = (line, args) => {
  // const { startIndex, version, reagents, units } = args;
  const fields = splitLine(line);
  switch (true) {
    case fields[0] === 'V':
      break;
    case fields[0] === 'P':
      break;
    case fields[0] === 'A' || fields[0] === 'T':
      break;
    case fields[0] === '#':
      break;
    case _.isEmpty(line):
      //  do absolutely nothig just sit there
      break;
    default:
  }
};
export const validateText = (text, args) => {
  let startIndex = 0;

  const lines = text.split('\n');

  lines.forEach(lines, (line, i) => {
    doYourThing(line, { ...args, startIndex });

    startIndex += line.length + 1;
  });
};
