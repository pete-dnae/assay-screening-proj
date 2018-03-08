import _ from 'lodash';
// stuff about painting tables goes here
export const formatText = (text) => {
  var finalText = '';
  const lines = text.split('\n');
  const wordPositions = { 0: [], 1: [], 2: [], 3: [], 4: [], 5: [] };
  lines.forEach((x) => {
    x.split(/\s+/).forEach((txt, i) => {
      if (i < 5) {
        wordPositions[i].push(txt);
      }
    });
  });

  const maxLength = _.reduce(
    wordPositions,
    (acc, x, i) => {
      if (!_.isEmpty(x)) {
        let longWord = _.maxBy(x, (a) => a.length);

        acc[i] = longWord.length;
      }

      return acc;
    },
    {},
  );

  lines.forEach((x) => {
    let finalLine = '';
    x.split(/\s+/).forEach((txt, i) => {
      const fillSpace = _.repeat(' ', maxLength[i] - txt.length);
      finalLine += `${txt} ${fillSpace}`;
    });
    finalText += `${finalLine.trimRight()}\n`;
  });
  return finalText;
};

export default formatText;
