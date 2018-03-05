import _ from 'lodash';

export const getToolTipPosition = (currentStyle, newBounds) => {
  const boundsInPixels = _.reduce(
    newBounds,
    (acc, x, i) => {
      acc[i] = `${x}px`;
      return acc;
    },
    {},
  );
  return { ...currentStyle, ...boundsInPixels };
};
