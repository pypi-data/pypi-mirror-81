(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[8497,768],{68497:(e,t,s)=>{"use strict";s.r(t);s.d(t,{AttachmentsModel:()=>r,AttachmentsResolver:()=>h});var a=s(10347);var i=s(30405);var n=s(63117);class r{constructor(e={}){this._map=new a.ObservableMap;this._isDisposed=false;this._stateChanged=new n.Signal(this);this._changed=new n.Signal(this);this._modelDB=null;this._serialized=null;this._changeGuard=false;this.contentFactory=e.contentFactory||r.defaultContentFactory;if(e.values){for(const t of Object.keys(e.values)){if(e.values[t]!==undefined){this.set(t,e.values[t])}}}this._map.changed.connect(this._onMapChanged,this);if(e.modelDB){this._modelDB=e.modelDB;this._serialized=this._modelDB.createValue("attachments");if(this._serialized.get()){this.fromJSON(this._serialized.get())}else{this._serialized.set(this.toJSON())}this._serialized.changed.connect(this._onSerializedChanged,this)}}get stateChanged(){return this._stateChanged}get changed(){return this._changed}get keys(){return this._map.keys()}get length(){return this._map.keys().length}get isDisposed(){return this._isDisposed}dispose(){if(this.isDisposed){return}this._isDisposed=true;this._map.dispose();n.Signal.clearData(this)}has(e){return this._map.has(e)}get(e){return this._map.get(e)}set(e,t){const s=this._createItem({value:t});this._map.set(e,s)}remove(e){this._map.delete(e)}clear(){this._map.values().forEach((e=>{e.dispose()}));this._map.clear()}fromJSON(e){this.clear();Object.keys(e).forEach((t=>{if(e[t]!==undefined){this.set(t,e[t])}}))}toJSON(){const e={};for(const t of this._map.keys()){e[t]=this._map.get(t).toJSON()}return e}_createItem(e){const t=this.contentFactory;const s=t.createAttachmentModel(e);s.changed.connect(this._onGenericChange,this);return s}_onMapChanged(e,t){if(this._serialized&&!this._changeGuard){this._changeGuard=true;this._serialized.set(this.toJSON());this._changeGuard=false}this._changed.emit(t);this._stateChanged.emit(void 0)}_onSerializedChanged(e,t){if(!this._changeGuard){this._changeGuard=true;this.fromJSON(t.newValue);this._changeGuard=false}}_onGenericChange(){this._stateChanged.emit(void 0)}}(function(e){class t{createAttachmentModel(e){return new i.AttachmentModel(e)}}e.ContentFactory=t;e.defaultContentFactory=new t})(r||(r={}));class h{constructor(e){this._parent=e.parent||null;this._model=e.model}resolveUrl(e){if(this._parent&&!e.startsWith("attachment:")){return this._parent.resolveUrl(e)}return Promise.resolve(e)}getDownloadUrl(e){if(this._parent&&!e.startsWith("attachment:")){return this._parent.getDownloadUrl(e)}const t=e.slice("attachment:".length);const s=this._model.get(t);if(s===undefined){return Promise.resolve(e)}const{data:a}=s;const n=Object.keys(a)[0];if(n===undefined||i.imageRendererFactory.mimeTypes.indexOf(n)===-1){return Promise.reject(`Cannot render unknown image mime type "${n}".`)}const r=`data:${n};base64,${a[n]}`;return Promise.resolve(r)}isLocal(e){var t,s,a;if(this._parent&&!e.startsWith("attachment:")){return(a=(s=(t=this._parent).isLocal)===null||s===void 0?void 0:s.call(t,e))!==null&&a!==void 0?a:true}return true}}}}]);