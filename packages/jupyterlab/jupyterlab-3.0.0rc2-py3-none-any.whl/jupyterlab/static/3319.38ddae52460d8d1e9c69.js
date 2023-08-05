(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[3319,8285],{83319:(t,e,s)=>{"use strict";s.r(e);s.d(e,{IInspector:()=>m,InspectionHandler:()=>c,InspectorPanel:()=>g,KernelConnector:()=>C});var n=s(61554);var i=s(30405);var o=s(23114);var r=s(63117);class c{constructor(t){this._cleared=new r.Signal(this);this._disposed=new r.Signal(this);this._editor=null;this._inspected=new r.Signal(this);this._isDisposed=false;this._pending=0;this._standby=true;this._connector=t.connector;this._rendermime=t.rendermime;this._debouncer=new o.Debouncer(this.onEditorChange.bind(this),250)}get cleared(){return this._cleared}get disposed(){return this._disposed}get inspected(){return this._inspected}get editor(){return this._editor}set editor(t){if(t===this._editor){return}r.Signal.disconnectReceiver(this);const e=this._editor=t;if(e){this._cleared.emit(void 0);this.onEditorChange();e.model.selections.changed.connect(this._onChange,this);e.model.value.changed.connect(this._onChange,this)}}get standby(){return this._standby}set standby(t){this._standby=t}get isDisposed(){return this._isDisposed}dispose(){if(this.isDisposed){return}this._isDisposed=true;this._disposed.emit(void 0);r.Signal.clearData(this)}onEditorChange(){if(this._standby){return}const t=this.editor;if(!t){return}const e=t.model.value.text;const s=t.getCursorPosition();const o=n.Text.jsIndexToCharIndex(t.getOffsetAt(s),e);const r={content:null};const c=++this._pending;void this._connector.fetch({offset:o,text:e}).then((t=>{if(!t||this.isDisposed||c!==this._pending){this._inspected.emit(r);return}const{data:e}=t;const s=this._rendermime.preferredMimeType(e);if(s){const t=this._rendermime.createRenderer(s);const n=new i.MimeModel({data:e});void t.renderModel(n);r.content=t}this._inspected.emit(r)})).catch((t=>{this._inspected.emit(r)}))}_onChange(){void this._debouncer.invoke()}}var d=s(84982);var a=s(49019);var h=s(52191);var u=s(93144);var l=s(86992);const p="jp-Inspector";const _="jp-Inspector-content";const f="jp-Inspector-default-content";class g extends l.Panel{constructor(t={}){super();this._source=null;this.translator=t.translator||u.nullTranslator;this._trans=this.translator.load("jupyterlab");if(t.initialContent instanceof l.Widget){this._content=t.initialContent}else if(typeof t.initialContent==="string"){this._content=g._generateContentWidget(`<p>${t.initialContent}</p>`)}else{this._content=g._generateContentWidget("<p>"+this._trans.__("Click on a function to see documentation.")+"</p>")}this.addClass(p);this.layout.addWidget(this._content)}[d.Printing.symbol](){return()=>d.Printing.printWidget(this)}get source(){return this._source}set source(t){if(this._source===t){return}if(this._source){this._source.standby=true;this._source.inspected.disconnect(this.onInspectorUpdate,this);this._source.disposed.disconnect(this.onSourceDisposed,this)}if(t&&t.isDisposed){t=null}this._source=t;if(this._source){this._source.standby=false;this._source.inspected.connect(this.onInspectorUpdate,this);this._source.disposed.connect(this.onSourceDisposed,this)}}dispose(){if(this.isDisposed){return}this.source=null;super.dispose()}onInspectorUpdate(t,e){const{content:s}=e;if(!s||s===this._content){return}this._content.dispose();this._content=s;s.addClass(_);this.layout.addWidget(s)}onSourceDisposed(t,e){this.source=null}static _generateContentWidget(t){const e=new l.Widget;e.node.innerHTML=t;e.addClass(_);e.addClass(f);return e}}class C extends a.DataConnector{constructor(t){super();this._sessionContext=t.sessionContext}fetch(t){var e;const s=(e=this._sessionContext.session)===null||e===void 0?void 0:e.kernel;if(!s){return Promise.reject(new Error("Inspection fetch requires a kernel."))}const n={code:t.text,cursor_pos:t.offset,detail_level:1};return s.requestInspect(n).then((t=>{const e=t.content;if(e.status!=="ok"||!e.found){throw new Error("Inspection fetch failed to return successfully.")}return{data:e.data,metadata:e.metadata}}))}}const m=new h.Token("@jupyterlab/inspector:IInspector")}}]);