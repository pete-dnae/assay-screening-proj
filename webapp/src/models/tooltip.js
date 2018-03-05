import _ from 'lodash';

export const getToolTipPosition = (currentStyle, newBounds, parentBounds) => {
  const top = `${newBounds.top + parentBounds.top}px`;
  const left = `${newBounds.left + parentBounds.left}px`;
  return { ...currentStyle, top, left };
};
