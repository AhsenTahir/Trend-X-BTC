"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
exports.id = "vendor-chunks/@smithy+url-parser@3.0.3";
exports.ids = ["vendor-chunks/@smithy+url-parser@3.0.3"];
exports.modules = {

/***/ "(rsc)/./node_modules/.pnpm/@smithy+url-parser@3.0.3/node_modules/@smithy/url-parser/dist-es/index.js":
/*!******************************************************************************************************!*\
  !*** ./node_modules/.pnpm/@smithy+url-parser@3.0.3/node_modules/@smithy/url-parser/dist-es/index.js ***!
  \******************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   parseUrl: () => (/* binding */ parseUrl)\n/* harmony export */ });\n/* harmony import */ var _smithy_querystring_parser__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @smithy/querystring-parser */ \"(rsc)/./node_modules/.pnpm/@smithy+querystring-parser@3.0.3/node_modules/@smithy/querystring-parser/dist-es/index.js\");\n\nconst parseUrl = (url) => {\n    if (typeof url === \"string\") {\n        return parseUrl(new URL(url));\n    }\n    const { hostname, pathname, port, protocol, search } = url;\n    let query;\n    if (search) {\n        query = (0,_smithy_querystring_parser__WEBPACK_IMPORTED_MODULE_0__.parseQueryString)(search);\n    }\n    return {\n        hostname,\n        port: port ? parseInt(port) : undefined,\n        protocol,\n        path: pathname,\n        query,\n    };\n};\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9ub2RlX21vZHVsZXMvLnBucG0vQHNtaXRoeSt1cmwtcGFyc2VyQDMuMC4zL25vZGVfbW9kdWxlcy9Ac21pdGh5L3VybC1wYXJzZXIvZGlzdC1lcy9pbmRleC5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUE4RDtBQUN2RDtBQUNQO0FBQ0E7QUFDQTtBQUNBLFlBQVksNkNBQTZDO0FBQ3pEO0FBQ0E7QUFDQSxnQkFBZ0IsNEVBQWdCO0FBQ2hDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BtYXJibGlzbS9uZXh0anMvLi9ub2RlX21vZHVsZXMvLnBucG0vQHNtaXRoeSt1cmwtcGFyc2VyQDMuMC4zL25vZGVfbW9kdWxlcy9Ac21pdGh5L3VybC1wYXJzZXIvZGlzdC1lcy9pbmRleC5qcz8xYWNlIl0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7IHBhcnNlUXVlcnlTdHJpbmcgfSBmcm9tIFwiQHNtaXRoeS9xdWVyeXN0cmluZy1wYXJzZXJcIjtcbmV4cG9ydCBjb25zdCBwYXJzZVVybCA9ICh1cmwpID0+IHtcbiAgICBpZiAodHlwZW9mIHVybCA9PT0gXCJzdHJpbmdcIikge1xuICAgICAgICByZXR1cm4gcGFyc2VVcmwobmV3IFVSTCh1cmwpKTtcbiAgICB9XG4gICAgY29uc3QgeyBob3N0bmFtZSwgcGF0aG5hbWUsIHBvcnQsIHByb3RvY29sLCBzZWFyY2ggfSA9IHVybDtcbiAgICBsZXQgcXVlcnk7XG4gICAgaWYgKHNlYXJjaCkge1xuICAgICAgICBxdWVyeSA9IHBhcnNlUXVlcnlTdHJpbmcoc2VhcmNoKTtcbiAgICB9XG4gICAgcmV0dXJuIHtcbiAgICAgICAgaG9zdG5hbWUsXG4gICAgICAgIHBvcnQ6IHBvcnQgPyBwYXJzZUludChwb3J0KSA6IHVuZGVmaW5lZCxcbiAgICAgICAgcHJvdG9jb2wsXG4gICAgICAgIHBhdGg6IHBhdGhuYW1lLFxuICAgICAgICBxdWVyeSxcbiAgICB9O1xufTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(rsc)/./node_modules/.pnpm/@smithy+url-parser@3.0.3/node_modules/@smithy/url-parser/dist-es/index.js\n");

/***/ })

};
;