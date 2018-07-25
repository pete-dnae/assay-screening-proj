export const Colors = {
  backgroundnames: {
    lightblue: '#add8e6',
    lightcyan: '#e0ffff',
    lightgreen: '#90ee90',
    lightgrey: '#d3d3d3',
    lightpink: '#ffb6c1',
    lightyellow: '#ffffe0',
    aqua: '#00ffff',
  },
  foregroundnames: {
    azure: '#f0ffff',
    beige: '#f5f5dc',
    black: '#000000',
    blue: '#0000ff',
    brown: '#a52a2a',
    cyan: '#00ffff',
    darkblue: '#00008b',
    darkcyan: '#008b8b',
    darkgrey: '#a9a9a9',
    darkgreen: '#006400',
    darkkhaki: '#bdb76b',
    darkmagenta: '#8b008b',
    darkolivegreen: '#556b2f',
    darkorange: '#ff8c00',
    darkorchid: '#9932cc',
    darkred: '#8b0000',
    darksalmon: '#e9967a',
    darkviolet: '#9400d3',
    fuchsia: '#ff00ff',
    gold: '#ffd700',
    green: '#008000',
    indigo: '#4b0082',
    khaki: '#f0e68c',
  },
  random(background) {
    let result;
    let count = 0;
    let names = this.foregroundnames;
    if (background) {
      names = this.backgroundnames;
    }
    for (const prop in names) {
      count += 1;

      if (Math.random() < 1 / count) {
        result = prop;
      }
    }

    return result;
  },
};


export default Colors;