export const splitLines = (arg, text) => text.split(arg);
export const validateRule = (dbData, concList, text) => {
  const feedback = {};
  const components = text.split(' ');
  const resultHtml = ["<div class='row'>"];
  if (components[0] === 'A' || components[0] === 'T') {
    resultHtml.push(`<p class='col'>${components[0]}</p>`);
  } else {
    feedback.rule_start = 'Invalid Rule Start : Should Start with A or T';
    resultHtml.push(
      `<p class="col text-danger">'Invalid Rule Start(${
        components[0]
      }) Should Start with A or T</p>`,
    );
  }

  if (dbData.includes(components[1].replace('@', ''))) {
    resultHtml.push(`<p class='col'>${components[1]}</p>`);
  } else {
    resultHtml.push(
      `<p class="col text-danger">Invalid Reagent Name(${components[1]})</p>`,
    );
  }
  if (
    /^\d+-\d+$/.test(components[2]) ||
    /^(?!,)(,?[0-9]+)+$/.test(components[2])
  ) {
    resultHtml.push(`<p class='col'>${components[2]}</p>`);
  } else {
    resultHtml.push(
      `<p class="col text-danger">Invalid Column Range(${components[2]})</p>`,
    );
  }
  if (
    /^[a-z A-Z]+-[a-z A-Z]+$/.test(components[3]) ||
    (/^(?!,)(,?[a-z A-Z]+)+$/.test(components[3]) && components[3])
  ) {
    resultHtml.push(`<p class='col'>${components[3]}</p>`);
  } else {
    resultHtml.push(
      `<p class="col text-danger">Invalid Row Range :(${components[3]})</p>`,
    );
  }
  if (concList.includes(components[5])) {
    resultHtml.push(`<p class='col'>${components[5]}</p>`);
  } else {
    resultHtml.push(
      `<p class="col text-danger">Invalid concentration unit :(${
        components[5]
      })</p>`,
    );
  }
  resultHtml.push('</div>');
  return { feedback, resultHtml };
};
