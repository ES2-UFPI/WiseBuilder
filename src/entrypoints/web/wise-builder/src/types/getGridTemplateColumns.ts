// arquivo getGridTemplateColumns.js
export default function getGridTemplateColumns() {
  const screenWidth = document.documentElement.clientWidth;
  if (screenWidth > 1024) {
    return "repeat(4, 1fr)";
  } else if (screenWidth > 768) {
    return "repeat(3, 1fr)";
  } else if (screenWidth > 480) {
    return "repeat(2, 1fr)";
  } else {
    return "1fr";
  }
}

  