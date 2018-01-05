export const zoomIn = (event) => {
  const element = document.getElementById('overlay');
  element.style.display = 'inline-block';
  const img = document.getElementById('imgZoom');
  const posX = event.offsetX ? event.offsetX : event.pageX - img.offsetLeft;
  const posY = event.offsetY ? event.offsetY : event.pageY - img.offsetTop;

  element.style.backgroundPosition = `${-posX * 2}px ${-posY * 4}px`;
};
export const zoomOut = () => {
  const element = document.getElementById('overlay');
  element.style.display = 'none';
};
