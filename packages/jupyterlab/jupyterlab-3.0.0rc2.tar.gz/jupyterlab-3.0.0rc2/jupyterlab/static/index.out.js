// This file is auto-generated from the corresponding file in /dev_mode
/*-----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

import {
  PageConfig,
  URLExt,
} from '@jupyterlab/coreutils';

// eslint-disable-next-line no-undef
__webpack_public_path__ = PageConfig.getOption('fullStaticUrl') + '/';

// Promise.allSettled polyfill, until our supported browsers implement it
// See https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled
if (Promise.allSettled === undefined) {
  Promise.allSettled = promises =>
    Promise.all(
      promises.map(promise =>
        promise
          .then(value => ({
            status: "fulfilled",
            value,
          }), reason => ({
            status: "rejected",
            reason,
          }))
      )
    );
}

// This must be after the public path is set.
// This cannot be extracted because the public path is dynamic.
require('./imports.css');


function loadScript(url) {
  return new Promise((resolve, reject) => {
    const newScript = document.createElement('script');
    newScript.onerror = reject;
    newScript.onload = resolve;
    newScript.async = true;
    document.head.appendChild(newScript);
    newScript.src = url;
  });
}

async function loadComponent(url, scope) {
  await loadScript(url);

  // From MIT-licensed https://github.com/module-federation/module-federation-examples/blob/af043acd6be1718ee195b2511adf6011fba4233c/advanced-api/dynamic-remotes/app1/src/App.js#L6-L12
  await __webpack_init_sharing__('default');
  const container = window._JUPYTERLAB[scope];
  // Initialize the container, it may provide shared modules and may need ours
  await container.init(__webpack_share_scopes__.default);
}

async function createModule(scope, module) {
  try {
    const factory = await window._JUPYTERLAB[scope].get(module);
    return factory();
  } catch(e) {
    console.warn(`Failed to create module: package: ${scope}; module: ${module}`);
    throw e;
  }
}

/**
 * The main entry point for the application.
 */
async function main() {
  var JupyterLab = require('@jupyterlab/application').JupyterLab;
  var disabled = [];
  var deferred = [];
  var ignorePlugins = [];
  var register = [];

  // This is all the data needed to load and activate plugins. This should be
  // gathered by the server and put onto the initial page template.
  const extension_data = JSON.parse(
    PageConfig.getOption('federated_extensions')
  );

  const federatedExtensionPromises = [];
  const federatedMimeExtensionPromises = [];
  const federatedStylePromises = [];

  // We first load all federated components so that the shared module
  // deduplication can run and figure out which shared modules from all
  // components should be actually used.
  const extensions = await Promise.allSettled(extension_data.map( async data => {
    await loadComponent(
      `${URLExt.join(PageConfig.getOption('fullLabextensionsUrl'), data.name, data.load)}`,
      data.name
    );
    return data;
  }));

  extensions.forEach(p => {
    if (p.status === "rejected") {
      // There was an error loading the component
      console.error(p.reason);
      return;
    }

    const data = p.value;
    if (data.extension) {
      federatedExtensionPromises.push(createModule(data.name, data.extension));
    }
    if (data.mimeExtension) {
      federatedMimeExtensionPromises.push(createModule(data.name, data.mimeExtension));
    }
    if (data.style) {
      federatedStylePromises.push(createModule(data.name, data.style));
    }
  });

  /**
   * Iterate over active plugins in an extension.
   * 
   * #### Notes
   * This also populates the disabled, deferred, and ignored arrays.
   */
  function* activePlugins(extension) {
    // Handle commonjs or es2015 modules
    let exports;
    if (extension.hasOwnProperty('__esModule')) {
      exports = extension.default;
    } else {
      // CommonJS exports.
      exports = extension;
    }

    let plugins = Array.isArray(exports) ? exports : [exports];
    for (let plugin of plugins) {
      if (PageConfig.Extension.isDisabled(plugin.id)) {
        disabled.push(plugin.id);
        continue;
      }
      if (PageConfig.Extension.isDeferred(plugin.id)) {
        deferred.push(plugin.id);
        ignorePlugins.push(plugin.id);
      }
      yield plugin;
    }
  }

  // Handle the registered mime extensions.
  const mimeExtensions = [];
  try {
    for (let plugin of activePlugins(require('@jupyterlab/javascript-extension/'))) {
      mimeExtensions.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/json-extension/'))) {
      mimeExtensions.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/pdf-extension/'))) {
      mimeExtensions.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/vega5-extension/'))) {
      mimeExtensions.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }

  // Add the federated mime extensions.
  const federatedMimeExtensions = await Promise.allSettled(federatedMimeExtensionPromises);
  federatedMimeExtensions.forEach(p => {
    if (p.status === "fulfilled") {
      for (let plugin of activePlugins(p.value)) {
        mimeExtensions.push(plugin);
      }
    } else {
      console.error(p.reason);
    }
  });

  // Handled the registered standard extensions.
  try {
    for (let plugin of activePlugins(require('@jupyterlab/application-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/apputils-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/celltags-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/codemirror-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/completer-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/console-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/csvviewer-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/debugger-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/docmanager-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/documentsearch-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/extensionmanager-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/filebrowser-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/fileeditor-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/help-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/htmlviewer-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/hub-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/imageviewer-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/inspector-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/launcher-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/logconsole-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/mainmenu-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/markdownviewer-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/mathjax2-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/notebook-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/rendermime-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/running-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/settingeditor-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/shortcuts-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/statusbar-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/terminal-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/theme-dark-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/theme-light-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/toc-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/tooltip-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/translation-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/ui-components-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }
  try {
    for (let plugin of activePlugins(require('@jupyterlab/vdom-extension/'))) {
      register.push(plugin);
    }
  } catch (e) {
    console.error(e);
  }

  // Add the federated extensions.
  const federatedExtensions = await Promise.allSettled(federatedExtensionPromises);
  federatedExtensions.forEach(p => {
    if (p.status === "fulfilled") {
      for (let plugin of activePlugins(p.value)) {
        register.push(plugin);
      }
    } else {
      console.error(p.reason);
    }
  });

  // Load all federated component styles and log errors for any that do not
  (await Promise.allSettled(federatedStylePromises)).filter(({status}) => status === "rejected").forEach(({reason}) => {
    console.error(reason);
  });

  const lab = new JupyterLab({
    mimeExtensions,
    disabled: {
      matches: disabled,
      patterns: PageConfig.Extension.disabled
        .map(function (val) { return val.raw; })
    },
    deferred: {
      matches: deferred,
      patterns: PageConfig.Extension.deferred
        .map(function (val) { return val.raw; })
    },
  });
  register.forEach(function(item) { lab.registerPluginModule(item); });
  lab.start({ ignorePlugins });

  // Expose global app instance when in dev mode or when toggled explicitly.
  var exposeAppInBrowser = (PageConfig.getOption('exposeAppInBrowser') || '').toLowerCase() === 'true';
  var devMode = (PageConfig.getOption('devMode') || '').toLowerCase() === 'true';

  if (exposeAppInBrowser || devMode) {
    window.jupyterlab = lab;
  }

  // Handle a browser test.
  var browserTest = PageConfig.getOption('browserTest');
  if (browserTest.toLowerCase() === 'true') {
    var el = document.createElement('div');
    el.id = 'browserTest';
    document.body.appendChild(el);
    el.textContent = '[]';
    el.style.display = 'none';
    var errors = [];
    var reported = false;
    var timeout = 25000;

    var report = function() {
      if (reported) {
        return;
      }
      reported = true;
      el.className = 'completed';
    }

    window.onerror = function(msg, url, line, col, error) {
      errors.push(String(error));
      el.textContent = JSON.stringify(errors)
    };
    console.error = function(message) {
      errors.push(String(message));
      el.textContent = JSON.stringify(errors)
    };

    lab.restored
      .then(function() { report(errors); })
      .catch(function(reason) { report([`RestoreError: ${reason.message}`]); });

    // Handle failures to restore after the timeout has elapsed.
    window.setTimeout(function() { report(errors); }, timeout);
  }

}

window.addEventListener('load', main);
