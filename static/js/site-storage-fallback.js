"use strict";

// Linkita's color script expects localStorage. Keep the theme usable when the
// browser blocks persistent storage by providing a per-page memory fallback.
(function () {
  try {
    var storage = window.localStorage;
    if (storage && typeof storage.getItem === "function") {
      var probeKey = "__john_cd_storage_probe_" + Math.random().toString(36).slice(2);
      storage.setItem(probeKey, "1");
      storage.removeItem(probeKey);
      return;
    }
  } catch (_error) {
    // Fall through to the in-memory adapter when storage is blocked or denied.
  }

  var values = new Map();
  var memoryStorage = {
    get length() {
      return values.size;
    },
    clear: function () {
      values.clear();
    },
    getItem: function (key) {
      key = String(key);
      return values.has(key) ? values.get(key) : null;
    },
    key: function (index) {
      var keys = Array.from(values.keys());
      var keyIndex = Number(index);
      keyIndex = keyIndex < 0 ? Math.ceil(keyIndex) : Math.floor(keyIndex);
      return keyIndex >= 0 && keyIndex < keys.length ? keys[keyIndex] : null;
    },
    removeItem: function (key) {
      values.delete(String(key));
    },
    setItem: function (key, value) {
      values.set(String(key), String(value));
    },
  };

  Object.defineProperty(window, "localStorage", {
    configurable: true,
    value: memoryStorage,
  });
})();
