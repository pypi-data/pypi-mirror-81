(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[8981,8731],{18981:(n,e,t)=>{"use strict";t.r(e);t.d(e,{IRunningSessionManagers:()=>L,RunningSessionManagers:()=>C,RunningSessions:()=>D});var a=t(52191);var s=t.n(a);var o=t(58578);var r=t.n(o);var l=t(10613);var i=t.n(l);var c=t(84982);var u=t.n(c);var m=t(93144);var g=t.n(m);var h=t(17651);var d=t.n(h);const p="jp-RunningSessions";const b="jp-RunningSessions-header";const w="jp-RunningSessions-section";const E="jp-RunningSessions-sectionHeader";const v="jp-RunningSessions-sectionContainer";const I="jp-RunningSessions-sectionList";const S="jp-RunningSessions-item";const _="jp-RunningSessions-itemLabel";const j="jp-RunningSessions-itemDetail";const R="jp-RunningSessions-itemShutdown";const f="jp-RunningSessions-shutdownAll";const L=new a.Token("@jupyterlab/running:IRunningSessionManagers");class C{constructor(){this._managers=[]}add(n){this._managers.push(n);return new o.DisposableDelegate((()=>{const e=this._managers.indexOf(n);if(e>-1){this._managers.splice(e,1)}}))}items(){return this._managers}}function k(n){var e;const{runningItem:t}=n;const a=t.icon();const s=(e=t.detail)===null||e===void 0?void 0:e.call(t);const o=n.translator||m.nullTranslator;const r=o.load("jupyterlab");const i=n.shutdownLabel||r.__("Shut Down");const u=n.shutdownItemIcon||h.closeIcon;return l.createElement("li",{className:S},l.createElement(a.react,{tag:"span",stylesheet:"runningItem"}),l.createElement("span",{className:_,title:t.labelTitle?t.labelTitle():"",onClick:()=>t.open()},t.label()),s&&l.createElement("span",{className:j},s),l.createElement(c.ToolbarButtonComponent,{className:R,icon:u,onClick:()=>t.shutdown(),tooltip:i}))}function y(n){return l.createElement("ul",{className:I},n.runningItems.map(((e,t)=>l.createElement(k,{key:t,runningItem:e,shutdownLabel:n.shutdownLabel,shutdownItemIcon:n.shutdownItemIcon,translator:n.translator}))))}function N(n){return l.createElement(c.UseSignal,{signal:n.manager.runningChanged},(()=>l.createElement(y,{runningItems:n.manager.running(),shutdownLabel:n.shutdownLabel,shutdownAllLabel:n.shutdownAllLabel,shutdownItemIcon:n.manager.shutdownItemIcon,translator:n.translator})))}function T(n){const e=n.translator||m.nullTranslator;const t=e.load("jupyterlab");const a=n.manager.shutdownAllLabel||t.__("Shut Down All");const s=`${a}?`;const o=n.manager.shutdownAllConfirmationText||`${a} ${n.manager.name}`;function r(){void(0,c.showDialog)({title:s,body:o,buttons:[c.Dialog.cancelButton({label:t.__("Cancel")}),c.Dialog.warnButton({label:a})]}).then((e=>{if(e.button.accept){n.manager.shutdownAll()}}))}return l.createElement("div",{className:w},l.createElement(l.Fragment,null,l.createElement("header",{className:E},l.createElement("h2",null,n.manager.name),l.createElement("button",{className:`${f} jp-mod-styled`,onClick:r},a)),l.createElement("div",{className:v},l.createElement(N,{manager:n.manager,shutdownLabel:n.manager.shutdownLabel,shutdownAllLabel:a,translator:n.translator}))))}function A(n){const e=n.translator||m.nullTranslator;const t=e.load("jupyterlab");return l.createElement(l.Fragment,null,l.createElement("div",{className:b},l.createElement(c.ToolbarButtonComponent,{tooltip:t.__("Refresh List"),icon:h.refreshIcon,onClick:()=>n.managers.items().forEach((n=>n.refreshRunning()))})),n.managers.items().map((e=>l.createElement(T,{key:e.name,manager:e,translator:n.translator}))))}class D extends c.ReactWidget{constructor(n,e){super();this.managers=n;this.translator=e||m.nullTranslator;this.addClass(p)}render(){return l.createElement(A,{managers:this.managers,translator:this.translator})}}}}]);