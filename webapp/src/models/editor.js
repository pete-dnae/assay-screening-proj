export const splitLines = (arg, text) => text.split(arg);
export const validateRule = (ruleNo, dbData, concList, text) => {
  const components = text.replace(/\s+/g, ' ').split(' ');
  const resultHtml = new Set();
  if (components[0] === 'A' || components[0] === 'T') {
    // empty
  } else {
    resultHtml.add(
      `<p class="row text-danger">'Invalid Rule Start(${
        components[0]
      }-Row ${ruleNo}) Should Start with A or T</p>`,
    );
  }

  if (dbData.includes(components[1])) {
    // empty
  } else {
    resultHtml.add(
      `<p class="row text-danger">Invalid Reagent Name(${
        components[1]
      }-Row ${ruleNo})</p>`,
    );
  }
  if (
    /^\d+-\d+$/.test(components[2]) ||
    /^(?!,)(,?[0-9]+)+$/.test(components[2])
  ) {
    // empty
  } else {
    resultHtml.add(
      `<p class="row text-danger">Invalid Column Range(${
        components[2]
      }-Row ${ruleNo})</p>`,
    );
  }
  if (
    /^[a-z A-Z]+-[a-z A-Z]+$/.test(components[3]) ||
    (/^(?!,)(,?[a-z A-Z]+)+$/.test(components[3]) && components[3])
  ) {
    // empty
  } else {
    resultHtml.add(
      `<p class="row text-danger">Invalid Row Range :(${
        components[3]
      }-Row ${ruleNo})</p>`,
    );
  }
  if (concList.includes(components[5])) {
    // empty
  } else {
    resultHtml.add(
      `<p class="row text-danger">Invalid concentration unit :(${
        components[5]
      }-Row ${ruleNo})</p>`,
    );
  }

  return resultHtml;
};
