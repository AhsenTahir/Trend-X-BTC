"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
exports.id = "vendor-chunks/@smithy+middleware-serde@3.0.3";
exports.ids = ["vendor-chunks/@smithy+middleware-serde@3.0.3"];
exports.modules = {

/***/ "(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/deserializerMiddleware.js":
/*!***********************************************************************************************************************************!*\
  !*** ./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/deserializerMiddleware.js ***!
  \***********************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   deserializerMiddleware: () => (/* binding */ deserializerMiddleware)\n/* harmony export */ });\nconst deserializerMiddleware = (options, deserializer) => (next) => async (args) => {\n    const { response } = await next(args);\n    try {\n        const parsed = await deserializer(response, options);\n        return {\n            response,\n            output: parsed,\n        };\n    }\n    catch (error) {\n        Object.defineProperty(error, \"$response\", {\n            value: response,\n        });\n        if (!(\"$metadata\" in error)) {\n            const hint = `Deserialization error: to see the raw response, inspect the hidden field {error}.$response on this object.`;\n            error.message += \"\\n  \" + hint;\n            if (typeof error.$responseBodyText !== \"undefined\") {\n                if (error.$response) {\n                    error.$response.body = error.$responseBodyText;\n                }\n            }\n        }\n        throw error;\n    }\n};\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9ub2RlX21vZHVsZXMvLnBucG0vQHNtaXRoeSttaWRkbGV3YXJlLXNlcmRlQDMuMC4zL25vZGVfbW9kdWxlcy9Ac21pdGh5L21pZGRsZXdhcmUtc2VyZGUvZGlzdC1lcy9kZXNlcmlhbGl6ZXJNaWRkbGV3YXJlLmpzIiwibWFwcGluZ3MiOiI7Ozs7QUFBTztBQUNQLFlBQVksV0FBVztBQUN2QjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBLG9HQUFvRyxNQUFNO0FBQzFHO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQG1hcmJsaXNtL25leHRqcy8uL25vZGVfbW9kdWxlcy8ucG5wbS9Ac21pdGh5K21pZGRsZXdhcmUtc2VyZGVAMy4wLjMvbm9kZV9tb2R1bGVzL0BzbWl0aHkvbWlkZGxld2FyZS1zZXJkZS9kaXN0LWVzL2Rlc2VyaWFsaXplck1pZGRsZXdhcmUuanM/ZWRkOSJdLCJzb3VyY2VzQ29udGVudCI6WyJleHBvcnQgY29uc3QgZGVzZXJpYWxpemVyTWlkZGxld2FyZSA9IChvcHRpb25zLCBkZXNlcmlhbGl6ZXIpID0+IChuZXh0KSA9PiBhc3luYyAoYXJncykgPT4ge1xuICAgIGNvbnN0IHsgcmVzcG9uc2UgfSA9IGF3YWl0IG5leHQoYXJncyk7XG4gICAgdHJ5IHtcbiAgICAgICAgY29uc3QgcGFyc2VkID0gYXdhaXQgZGVzZXJpYWxpemVyKHJlc3BvbnNlLCBvcHRpb25zKTtcbiAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICAgIHJlc3BvbnNlLFxuICAgICAgICAgICAgb3V0cHV0OiBwYXJzZWQsXG4gICAgICAgIH07XG4gICAgfVxuICAgIGNhdGNoIChlcnJvcikge1xuICAgICAgICBPYmplY3QuZGVmaW5lUHJvcGVydHkoZXJyb3IsIFwiJHJlc3BvbnNlXCIsIHtcbiAgICAgICAgICAgIHZhbHVlOiByZXNwb25zZSxcbiAgICAgICAgfSk7XG4gICAgICAgIGlmICghKFwiJG1ldGFkYXRhXCIgaW4gZXJyb3IpKSB7XG4gICAgICAgICAgICBjb25zdCBoaW50ID0gYERlc2VyaWFsaXphdGlvbiBlcnJvcjogdG8gc2VlIHRoZSByYXcgcmVzcG9uc2UsIGluc3BlY3QgdGhlIGhpZGRlbiBmaWVsZCB7ZXJyb3J9LiRyZXNwb25zZSBvbiB0aGlzIG9iamVjdC5gO1xuICAgICAgICAgICAgZXJyb3IubWVzc2FnZSArPSBcIlxcbiAgXCIgKyBoaW50O1xuICAgICAgICAgICAgaWYgKHR5cGVvZiBlcnJvci4kcmVzcG9uc2VCb2R5VGV4dCAhPT0gXCJ1bmRlZmluZWRcIikge1xuICAgICAgICAgICAgICAgIGlmIChlcnJvci4kcmVzcG9uc2UpIHtcbiAgICAgICAgICAgICAgICAgICAgZXJyb3IuJHJlc3BvbnNlLmJvZHkgPSBlcnJvci4kcmVzcG9uc2VCb2R5VGV4dDtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgdGhyb3cgZXJyb3I7XG4gICAgfVxufTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/deserializerMiddleware.js\n");

/***/ }),

/***/ "(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/index.js":
/*!******************************************************************************************************************!*\
  !*** ./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/index.js ***!
  \******************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   deserializerMiddleware: () => (/* reexport safe */ _deserializerMiddleware__WEBPACK_IMPORTED_MODULE_0__.deserializerMiddleware),\n/* harmony export */   deserializerMiddlewareOption: () => (/* reexport safe */ _serdePlugin__WEBPACK_IMPORTED_MODULE_1__.deserializerMiddlewareOption),\n/* harmony export */   getSerdePlugin: () => (/* reexport safe */ _serdePlugin__WEBPACK_IMPORTED_MODULE_1__.getSerdePlugin),\n/* harmony export */   serializerMiddleware: () => (/* reexport safe */ _serializerMiddleware__WEBPACK_IMPORTED_MODULE_2__.serializerMiddleware),\n/* harmony export */   serializerMiddlewareOption: () => (/* reexport safe */ _serdePlugin__WEBPACK_IMPORTED_MODULE_1__.serializerMiddlewareOption)\n/* harmony export */ });\n/* harmony import */ var _deserializerMiddleware__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./deserializerMiddleware */ \"(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/deserializerMiddleware.js\");\n/* harmony import */ var _serdePlugin__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./serdePlugin */ \"(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/serdePlugin.js\");\n/* harmony import */ var _serializerMiddleware__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./serializerMiddleware */ \"(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/serializerMiddleware.js\");\n\n\n\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9ub2RlX21vZHVsZXMvLnBucG0vQHNtaXRoeSttaWRkbGV3YXJlLXNlcmRlQDMuMC4zL25vZGVfbW9kdWxlcy9Ac21pdGh5L21pZGRsZXdhcmUtc2VyZGUvZGlzdC1lcy9pbmRleC5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUF5QztBQUNYO0FBQ1MiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AbWFyYmxpc20vbmV4dGpzLy4vbm9kZV9tb2R1bGVzLy5wbnBtL0BzbWl0aHkrbWlkZGxld2FyZS1zZXJkZUAzLjAuMy9ub2RlX21vZHVsZXMvQHNtaXRoeS9taWRkbGV3YXJlLXNlcmRlL2Rpc3QtZXMvaW5kZXguanM/MWRiOCJdLCJzb3VyY2VzQ29udGVudCI6WyJleHBvcnQgKiBmcm9tIFwiLi9kZXNlcmlhbGl6ZXJNaWRkbGV3YXJlXCI7XG5leHBvcnQgKiBmcm9tIFwiLi9zZXJkZVBsdWdpblwiO1xuZXhwb3J0ICogZnJvbSBcIi4vc2VyaWFsaXplck1pZGRsZXdhcmVcIjtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/index.js\n");

/***/ }),

/***/ "(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/serdePlugin.js":
/*!************************************************************************************************************************!*\
  !*** ./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/serdePlugin.js ***!
  \************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   deserializerMiddlewareOption: () => (/* binding */ deserializerMiddlewareOption),\n/* harmony export */   getSerdePlugin: () => (/* binding */ getSerdePlugin),\n/* harmony export */   serializerMiddlewareOption: () => (/* binding */ serializerMiddlewareOption)\n/* harmony export */ });\n/* harmony import */ var _deserializerMiddleware__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./deserializerMiddleware */ \"(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/deserializerMiddleware.js\");\n/* harmony import */ var _serializerMiddleware__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./serializerMiddleware */ \"(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/serializerMiddleware.js\");\n\n\nconst deserializerMiddlewareOption = {\n    name: \"deserializerMiddleware\",\n    step: \"deserialize\",\n    tags: [\"DESERIALIZER\"],\n    override: true,\n};\nconst serializerMiddlewareOption = {\n    name: \"serializerMiddleware\",\n    step: \"serialize\",\n    tags: [\"SERIALIZER\"],\n    override: true,\n};\nfunction getSerdePlugin(config, serializer, deserializer) {\n    return {\n        applyToStack: (commandStack) => {\n            commandStack.add((0,_deserializerMiddleware__WEBPACK_IMPORTED_MODULE_0__.deserializerMiddleware)(config, deserializer), deserializerMiddlewareOption);\n            commandStack.add((0,_serializerMiddleware__WEBPACK_IMPORTED_MODULE_1__.serializerMiddleware)(config, serializer), serializerMiddlewareOption);\n        },\n    };\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9ub2RlX21vZHVsZXMvLnBucG0vQHNtaXRoeSttaWRkbGV3YXJlLXNlcmRlQDMuMC4zL25vZGVfbW9kdWxlcy9Ac21pdGh5L21pZGRsZXdhcmUtc2VyZGUvZGlzdC1lcy9zZXJkZVBsdWdpbi5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFrRTtBQUNKO0FBQ3ZEO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNPO0FBQ1A7QUFDQTtBQUNBLDZCQUE2QiwrRUFBc0I7QUFDbkQsNkJBQTZCLDJFQUFvQjtBQUNqRCxTQUFTO0FBQ1Q7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BtYXJibGlzbS9uZXh0anMvLi9ub2RlX21vZHVsZXMvLnBucG0vQHNtaXRoeSttaWRkbGV3YXJlLXNlcmRlQDMuMC4zL25vZGVfbW9kdWxlcy9Ac21pdGh5L21pZGRsZXdhcmUtc2VyZGUvZGlzdC1lcy9zZXJkZVBsdWdpbi5qcz84ZDA1Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7IGRlc2VyaWFsaXplck1pZGRsZXdhcmUgfSBmcm9tIFwiLi9kZXNlcmlhbGl6ZXJNaWRkbGV3YXJlXCI7XG5pbXBvcnQgeyBzZXJpYWxpemVyTWlkZGxld2FyZSB9IGZyb20gXCIuL3NlcmlhbGl6ZXJNaWRkbGV3YXJlXCI7XG5leHBvcnQgY29uc3QgZGVzZXJpYWxpemVyTWlkZGxld2FyZU9wdGlvbiA9IHtcbiAgICBuYW1lOiBcImRlc2VyaWFsaXplck1pZGRsZXdhcmVcIixcbiAgICBzdGVwOiBcImRlc2VyaWFsaXplXCIsXG4gICAgdGFnczogW1wiREVTRVJJQUxJWkVSXCJdLFxuICAgIG92ZXJyaWRlOiB0cnVlLFxufTtcbmV4cG9ydCBjb25zdCBzZXJpYWxpemVyTWlkZGxld2FyZU9wdGlvbiA9IHtcbiAgICBuYW1lOiBcInNlcmlhbGl6ZXJNaWRkbGV3YXJlXCIsXG4gICAgc3RlcDogXCJzZXJpYWxpemVcIixcbiAgICB0YWdzOiBbXCJTRVJJQUxJWkVSXCJdLFxuICAgIG92ZXJyaWRlOiB0cnVlLFxufTtcbmV4cG9ydCBmdW5jdGlvbiBnZXRTZXJkZVBsdWdpbihjb25maWcsIHNlcmlhbGl6ZXIsIGRlc2VyaWFsaXplcikge1xuICAgIHJldHVybiB7XG4gICAgICAgIGFwcGx5VG9TdGFjazogKGNvbW1hbmRTdGFjaykgPT4ge1xuICAgICAgICAgICAgY29tbWFuZFN0YWNrLmFkZChkZXNlcmlhbGl6ZXJNaWRkbGV3YXJlKGNvbmZpZywgZGVzZXJpYWxpemVyKSwgZGVzZXJpYWxpemVyTWlkZGxld2FyZU9wdGlvbik7XG4gICAgICAgICAgICBjb21tYW5kU3RhY2suYWRkKHNlcmlhbGl6ZXJNaWRkbGV3YXJlKGNvbmZpZywgc2VyaWFsaXplciksIHNlcmlhbGl6ZXJNaWRkbGV3YXJlT3B0aW9uKTtcbiAgICAgICAgfSxcbiAgICB9O1xufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/serdePlugin.js\n");

/***/ }),

/***/ "(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/serializerMiddleware.js":
/*!*********************************************************************************************************************************!*\
  !*** ./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/serializerMiddleware.js ***!
  \*********************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   serializerMiddleware: () => (/* binding */ serializerMiddleware)\n/* harmony export */ });\nconst serializerMiddleware = (options, serializer) => (next, context) => async (args) => {\n    const endpoint = context.endpointV2?.url && options.urlParser\n        ? async () => options.urlParser(context.endpointV2.url)\n        : options.endpoint;\n    if (!endpoint) {\n        throw new Error(\"No valid endpoint provider available.\");\n    }\n    const request = await serializer(args.input, { ...options, endpoint });\n    return next({\n        ...args,\n        request,\n    });\n};\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9ub2RlX21vZHVsZXMvLnBucG0vQHNtaXRoeSttaWRkbGV3YXJlLXNlcmRlQDMuMC4zL25vZGVfbW9kdWxlcy9Ac21pdGh5L21pZGRsZXdhcmUtc2VyZGUvZGlzdC1lcy9zZXJpYWxpemVyTWlkZGxld2FyZS5qcyIsIm1hcHBpbmdzIjoiOzs7O0FBQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxtREFBbUQsc0JBQXNCO0FBQ3pFO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTCIsInNvdXJjZXMiOlsid2VicGFjazovL0BtYXJibGlzbS9uZXh0anMvLi9ub2RlX21vZHVsZXMvLnBucG0vQHNtaXRoeSttaWRkbGV3YXJlLXNlcmRlQDMuMC4zL25vZGVfbW9kdWxlcy9Ac21pdGh5L21pZGRsZXdhcmUtc2VyZGUvZGlzdC1lcy9zZXJpYWxpemVyTWlkZGxld2FyZS5qcz9jMzA0Il0sInNvdXJjZXNDb250ZW50IjpbImV4cG9ydCBjb25zdCBzZXJpYWxpemVyTWlkZGxld2FyZSA9IChvcHRpb25zLCBzZXJpYWxpemVyKSA9PiAobmV4dCwgY29udGV4dCkgPT4gYXN5bmMgKGFyZ3MpID0+IHtcbiAgICBjb25zdCBlbmRwb2ludCA9IGNvbnRleHQuZW5kcG9pbnRWMj8udXJsICYmIG9wdGlvbnMudXJsUGFyc2VyXG4gICAgICAgID8gYXN5bmMgKCkgPT4gb3B0aW9ucy51cmxQYXJzZXIoY29udGV4dC5lbmRwb2ludFYyLnVybClcbiAgICAgICAgOiBvcHRpb25zLmVuZHBvaW50O1xuICAgIGlmICghZW5kcG9pbnQpIHtcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKFwiTm8gdmFsaWQgZW5kcG9pbnQgcHJvdmlkZXIgYXZhaWxhYmxlLlwiKTtcbiAgICB9XG4gICAgY29uc3QgcmVxdWVzdCA9IGF3YWl0IHNlcmlhbGl6ZXIoYXJncy5pbnB1dCwgeyAuLi5vcHRpb25zLCBlbmRwb2ludCB9KTtcbiAgICByZXR1cm4gbmV4dCh7XG4gICAgICAgIC4uLmFyZ3MsXG4gICAgICAgIHJlcXVlc3QsXG4gICAgfSk7XG59O1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///(rsc)/./node_modules/.pnpm/@smithy+middleware-serde@3.0.3/node_modules/@smithy/middleware-serde/dist-es/serializerMiddleware.js\n");

/***/ })

};
;