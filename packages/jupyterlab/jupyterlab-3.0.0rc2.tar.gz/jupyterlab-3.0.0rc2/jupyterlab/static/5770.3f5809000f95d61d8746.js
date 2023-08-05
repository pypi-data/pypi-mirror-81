(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[5770],{5770:(e,t,i)=>{"use strict";i.r(t);i.d(t,{ABCWidgetFactory:()=>F,Base64ModelFactory:()=>y,Context:()=>c,DocumentModel:()=>g,DocumentRegistry:()=>S,DocumentWidget:()=>w,MimeContent:()=>b,MimeDocument:()=>T,MimeDocumentFactory:()=>C,TextModelFactory:()=>f});var s=i(52191);var n=i(58578);var a=i(63117);var r=i(86992);var o=i(84982);var h=i(61554);var l=i(30405);var d=i(93144);class c{constructor(e){this._path="";this._useCRLF=false;this._contentsModel=null;this._populatedPromise=new s.PromiseDelegate;this._isPopulated=false;this._isReady=false;this._isDisposed=false;this._pathChanged=new a.Signal(this);this._fileChanged=new a.Signal(this);this._saveState=new a.Signal(this);this._disposed=new a.Signal(this);const t=this._manager=e.manager;this.translator=e.translator||d.nullTranslator;this._trans=this.translator.load("jupyterlab");this._factory=e.factory;this._dialogs=e.sessionDialogs||o.sessionContextDialogs;this._opener=e.opener||_.noOp;this._path=this._manager.contents.normalize(e.path);const i=this._manager.contents.localPath(this._path);const n=this._factory.preferredLanguage(h.PathExt.basename(i));const r=e.modelDBFactory;if(r){const e=t.contents.localPath(this._path);this._modelDB=r.createNew(e);this._model=this._factory.createNew(n,this._modelDB)}else{this._model=this._factory.createNew(n)}this._readyPromise=t.ready.then((()=>this._populatedPromise.promise));const c=h.PathExt.extname(this._path);this.sessionContext=new o.SessionContext({sessionManager:t.sessions,specsManager:t.kernelspecs,path:this._path,type:c===".ipynb"?"notebook":"file",name:h.PathExt.basename(i),kernelPreference:e.kernelPreference||{shouldStart:false},setBusy:e.setBusy});this.sessionContext.propertyChanged.connect(this._onSessionChanged,this);t.contents.fileChanged.connect(this._onFileChanged,this);const u=this.urlResolver=new l.RenderMimeRegistry.UrlResolver({path:this._path,contents:t.contents});this.pathChanged.connect(((e,t)=>{u.path=t}))}get pathChanged(){return this._pathChanged}get fileChanged(){return this._fileChanged}get saveState(){return this._saveState}get disposed(){return this._disposed}get model(){return this._model}get path(){return this._path}get localPath(){return this._manager.contents.localPath(this._path)}get contentsModel(){return this._contentsModel}get factoryName(){return this.isDisposed?"":this._factory.name}get isDisposed(){return this._isDisposed}dispose(){if(this.isDisposed){return}this._isDisposed=true;this.sessionContext.dispose();if(this._modelDB){this._modelDB.dispose()}this._model.dispose();this._disposed.emit(void 0);a.Signal.clearData(this)}get isReady(){return this._isReady}get ready(){return this._readyPromise}initialize(e){if(e){this._model.initialize();return this._save()}if(this._modelDB){return this._modelDB.connected.then((()=>{if(this._modelDB.isPrepopulated){this._model.initialize();void this._save();return void 0}else{return this._revert(true)}}))}else{return this._revert(true)}}save(){return this.ready.then((()=>this._save()))}saveAs(){return this.ready.then((()=>_.getSavePath(this._path))).then((e=>{if(this.isDisposed||!e){return}if(e===this._path){return this.save()}return this._manager.ready.then((()=>this._manager.contents.get(e))).then((()=>this._maybeOverWrite(e))).catch((t=>{if(!t.response||t.response.status!==404){throw t}return this._finishSaveAs(e)}))}))}async download(){const e=await this._manager.contents.getDownloadUrl(this._path);const t=document.createElement("a");t.href=e;t.download="";document.body.appendChild(t);t.click();document.body.removeChild(t);return void 0}revert(){return this.ready.then((()=>this._revert()))}createCheckpoint(){const e=this._manager.contents;return this._manager.ready.then((()=>e.createCheckpoint(this._path)))}deleteCheckpoint(e){const t=this._manager.contents;return this._manager.ready.then((()=>t.deleteCheckpoint(this._path,e)))}restoreCheckpoint(e){const t=this._manager.contents;const i=this._path;return this._manager.ready.then((()=>{if(e){return t.restoreCheckpoint(i,e)}return this.listCheckpoints().then((s=>{if(this.isDisposed||!s.length){return}e=s[s.length-1].id;return t.restoreCheckpoint(i,e)}))}))}listCheckpoints(){const e=this._manager.contents;return this._manager.ready.then((()=>e.listCheckpoints(this._path)))}addSibling(e,t={}){const i=this._opener;if(i){i(e,t)}return new n.DisposableDelegate((()=>{e.close()}))}_onFileChanged(e,t){var i,s,n;if(t.type!=="rename"){return}let a=t.oldValue&&t.oldValue.path;let r=t.newValue&&t.newValue.path;if(r&&this._path.indexOf(a||"")===0){let e=t.newValue;if(a!==this._path){r=this._path.replace(new RegExp(`^${a}/`),`${r}/`);a=this._path;e={last_modified:(i=t.newValue)===null||i===void 0?void 0:i.created,path:r}}this._path=r;void((s=this.sessionContext.session)===null||s===void 0?void 0:s.setPath(r));const o=Object.assign(Object.assign({},this._contentsModel),e);const l=this._manager.contents.localPath(r);void((n=this.sessionContext.session)===null||n===void 0?void 0:n.setName(h.PathExt.basename(l)));this._updateContentsModel(o);this._pathChanged.emit(this._path)}}_onSessionChanged(e,t){if(t!=="path"){return}const i=this.sessionContext.session.path;if(i!==this._path){this._path=i;this._pathChanged.emit(i)}}_updateContentsModel(e){const t={path:e.path,name:e.name,type:e.type,content:undefined,writable:e.writable,created:e.created,last_modified:e.last_modified,mimetype:e.mimetype,format:e.format};const i=this._contentsModel?this._contentsModel.last_modified:null;this._contentsModel=t;if(!i||t.last_modified!==i){this._fileChanged.emit(t)}}_populate(){this._isPopulated=true;this._isReady=true;this._populatedPromise.resolve(void 0);return this._maybeCheckpoint(false).then((()=>{if(this.isDisposed){return}const e=this._model.defaultKernelName||this.sessionContext.kernelPreference.name;this.sessionContext.kernelPreference=Object.assign(Object.assign({},this.sessionContext.kernelPreference),{name:e,language:this._model.defaultKernelLanguage});void this.sessionContext.initialize().then((e=>{if(e){void this._dialogs.selectKernel(this.sessionContext)}}))}))}async _save(){this._saveState.emit("started");const e=this._model;let t;if(this._factory.fileFormat==="json"){t=e.toJSON()}else{t=e.toString();if(this._useCRLF){t=t.replace(/\n/g,"\r\n")}}const i={type:this._factory.contentType,format:this._factory.fileFormat,content:t};try{let t;await this._manager.ready;if(!e.modelDB.isCollaborative){t=await this._maybeSave(i)}else{t=await this._manager.contents.save(this._path,i)}if(this.isDisposed){return}e.dirty=false;this._updateContentsModel(t);if(!this._isPopulated){await this._populate()}this._saveState.emit("completed")}catch(s){if(s.message==="Cancel"){throw s}const e=this._manager.contents.localPath(this._path);const t=h.PathExt.basename(e);void this._handleError(s,this._trans.__("File Save Error for %1",t));this._saveState.emit("failed");throw s}}_revert(e=false){const t={format:this._factory.fileFormat,type:this._factory.contentType,content:true};const i=this._path;const s=this._model;return this._manager.ready.then((()=>this._manager.contents.get(i,t))).then((t=>{if(this.isDisposed){return}const i=false;if(t.format==="json"){s.fromJSON(t.content);if(e){s.initialize()}}else{let i=t.content;if(i.indexOf("\r")!==-1){this._useCRLF=true;i=i.replace(/\r\n/g,"\n")}else{this._useCRLF=false}s.fromString(i);if(e){s.initialize()}}this._updateContentsModel(t);s.dirty=i;if(!this._isPopulated){return this._populate()}})).catch((async e=>{const t=this._manager.contents.localPath(this._path);const i=h.PathExt.basename(t);void this._handleError(e,this._trans.__("File Load Error for %1",i));throw e}))}_maybeSave(e){const t=this._path;const i=this._manager.contents.get(t,{content:false});return i.then((i=>{var s;if(this.isDisposed){return Promise.reject(new Error("Disposed"))}const n=(s=this.contentsModel)===null||s===void 0?void 0:s.last_modified;const a=n?new Date(n):new Date;const r=new Date(i.last_modified);if(n&&r.getTime()-a.getTime()>500){return this._timeConflict(a,i,e)}return this._manager.contents.save(t,e)}),(i=>{if(i.response&&i.response.status===404){return this._manager.contents.save(t,e)}throw i}))}async _handleError(e,t){await(0,o.showErrorMessage)(t,e);return}_maybeCheckpoint(e){let t=this._contentsModel&&this._contentsModel.writable;let i=Promise.resolve(void 0);if(!t){return i}if(e){i=this.createCheckpoint().then()}else{i=this.listCheckpoints().then((e=>{t=this._contentsModel&&this._contentsModel.writable;if(!this.isDisposed&&!e.length&&t){return this.createCheckpoint().then()}}))}return i.catch((e=>{if(!e.response||e.response.status!==403){throw e}}))}_timeConflict(e,t,i){const s=new Date(t.last_modified);console.warn(`Last saving performed ${e} `+`while the current file seems to have been saved `+`${s}`);const n=this._trans.__(`"%1" has changed on disk since the last time it was opened or saved.\nDo you want to overwrite the file on disk with the version open here, \nor load the version on disk (revert)?`,this.path);const a=o.Dialog.okButton({label:this._trans.__("Revert")});const r=o.Dialog.warnButton({label:this._trans.__("Overwrite")});return(0,o.showDialog)({title:this._trans.__("File Changed"),body:n,buttons:[o.Dialog.cancelButton(),a,r]}).then((e=>{if(this.isDisposed){return Promise.reject(new Error("Disposed"))}if(e.button.label===this._trans.__("Overwrite")){return this._manager.contents.save(this._path,i)}if(e.button.label===this._trans.__("Revert")){return this.revert().then((()=>t))}return Promise.reject(new Error("Cancel"))}))}_maybeOverWrite(e){const t=this._trans.__('"%1" already exists. Do you want to replace it?',e);const i=o.Dialog.warnButton({label:this._trans.__("Overwrite")});return(0,o.showDialog)({title:this._trans.__("File Overwrite?"),body:t,buttons:[o.Dialog.cancelButton(),i]}).then((t=>{if(this.isDisposed){return Promise.reject(new Error("Disposed"))}if(t.button.label===this._trans.__("Overwrite")){return this._manager.contents.delete(e).then((()=>this._finishSaveAs(e)))}}))}async _finishSaveAs(e){var t,i;this._path=e;await((t=this.sessionContext.session)===null||t===void 0?void 0:t.setPath(e));await((i=this.sessionContext.session)===null||i===void 0?void 0:i.setName(e.split("/").pop()));await this.save();this._pathChanged.emit(this._path);await this._maybeCheckpoint(true)}}var _;(function(e){function t(e,t){t=t||d.nullTranslator;const i=t.load("jupyterlab");const n=o.Dialog.okButton({label:i.__("Save")});return(0,o.showDialog)({title:i.__("Save File As.."),body:new s(e),buttons:[o.Dialog.cancelButton(),n]}).then((e=>{var t;if(e.button.label===i.__("Save")){return(t=e.value)!==null&&t!==void 0?t:undefined}return}))}e.getSavePath=t;function i(){}e.noOp=i;class s extends r.Widget{constructor(e){super({node:n(e)})}getValue(){return this.node.value}}function n(e){const t=document.createElement("input");t.value=e;return t}})(_||(_={}));var u=i(3123);var m=i(93269);var p=i(97432);class g extends p.CodeEditor.Model{constructor(e,t){super({modelDB:t});this._defaultLang="";this._dirty=false;this._readOnly=false;this._contentChanged=new a.Signal(this);this._stateChanged=new a.Signal(this);this._defaultLang=e||"";this.value.changed.connect(this.triggerContentChange,this)}get contentChanged(){return this._contentChanged}get stateChanged(){return this._stateChanged}get dirty(){return this._dirty}set dirty(e){if(e===this._dirty){return}const t=this._dirty;this._dirty=e;this.triggerStateChange({name:"dirty",oldValue:t,newValue:e})}get readOnly(){return this._readOnly}set readOnly(e){if(e===this._readOnly){return}const t=this._readOnly;this._readOnly=e;this.triggerStateChange({name:"readOnly",oldValue:t,newValue:e})}get defaultKernelName(){return""}get defaultKernelLanguage(){return this._defaultLang}toString(){return this.value.text}fromString(e){this.value.text=e}toJSON(){return JSON.parse(this.value.text||"null")}fromJSON(e){this.fromString(JSON.stringify(e))}initialize(){return}triggerStateChange(e){this._stateChanged.emit(e)}triggerContentChange(){this._contentChanged.emit(void 0);this.dirty=true}}class f{constructor(){this._isDisposed=false}get name(){return"text"}get contentType(){return"file"}get fileFormat(){return"text"}get isDisposed(){return this._isDisposed}dispose(){this._isDisposed=true}createNew(e,t){return new g(e,t)}preferredLanguage(e){const t=u.Mode.findByFileName(e);return t&&t.mode}}class y extends f{get name(){return"base64"}get contentType(){return"file"}get fileFormat(){return"base64"}}class F{constructor(e){this._isDisposed=false;this._widgetCreated=new a.Signal(this);this._translator=e.translator||d.nullTranslator;this._name=e.name;this._readOnly=e.readOnly===undefined?false:e.readOnly;this._defaultFor=e.defaultFor?e.defaultFor.slice():[];this._defaultRendered=(e.defaultRendered||[]).slice();this._fileTypes=e.fileTypes.slice();this._modelName=e.modelName||"text";this._preferKernel=!!e.preferKernel;this._canStartKernel=!!e.canStartKernel;this._shutdownOnClose=!!e.shutdownOnClose;this._toolbarFactory=e.toolbarFactory}get widgetCreated(){return this._widgetCreated}get isDisposed(){return this._isDisposed}dispose(){if(this.isDisposed){return}this._isDisposed=true;a.Signal.clearData(this)}get readOnly(){return this._readOnly}get name(){return this._name}get fileTypes(){return this._fileTypes.slice()}get modelName(){return this._modelName}get defaultFor(){return this._defaultFor.slice()}get defaultRendered(){return this._defaultRendered.slice()}get preferKernel(){return this._preferKernel}get canStartKernel(){return this._canStartKernel}get translator(){return this._translator}get shutdownOnClose(){return this._shutdownOnClose}set shutdownOnClose(e){this._shutdownOnClose=e}createNew(e,t){const i=this.createNewWidget(e,t);let s;if(this._toolbarFactory){s=this._toolbarFactory(i)}else{s=this.defaultToolbarFactory(i)}s.forEach((({name:e,widget:t})=>{i.toolbar.addItem(e,t)}));this._widgetCreated.emit(i);return i}defaultToolbarFactory(e){return[]}}const v="jp-mod-dirty";class w extends o.MainAreaWidget{constructor(e){e.reveal=Promise.all([e.reveal,e.context.ready]);super(e);this.context=e.context;this.context.pathChanged.connect(this._onPathChanged,this);this._onPathChanged(this.context,this.context.path);this.context.model.stateChanged.connect(this._onModelStateChanged,this);void this.context.ready.then((()=>{this._handleDirtyState()}))}setFragment(e){}_onPathChanged(e,t){this.title.label=h.PathExt.basename(e.localPath)}_onModelStateChanged(e,t){if(t.name==="dirty"){this._handleDirtyState()}}_handleDirtyState(){if(this.context.model.dirty){this.title.className+=` ${v}`}else{this.title.className=this.title.className.replace(v,"")}}}var x=i(74723);class b extends r.Widget{constructor(e){super();this._changeCallback=e=>{if(!e.data||!e.data[this.mimeType]){return}const t=e.data[this.mimeType];if(typeof t==="string"){if(t!==this._context.model.toString()){this._context.model.fromString(t)}}else if(t!==null&&t!==undefined&&!s.JSONExt.deepEqual(t,this._context.model.toJSON())){this._context.model.fromJSON(t)}};this._fragment="";this._ready=new s.PromiseDelegate;this._isRendering=false;this._renderRequested=false;this.addClass("jp-MimeDocument");this.translator=e.translator||d.nullTranslator;this._trans=this.translator.load("jupyterlab");this.mimeType=e.mimeType;this._dataType=e.dataType||"string";this._context=e.context;this.renderer=e.renderer;const t=this.layout=new r.StackedLayout;t.addWidget(this.renderer);this._context.ready.then((()=>this._render())).then((()=>{if(this.node===document.activeElement){x.MessageLoop.sendMessage(this.renderer,r.Widget.Msg.ActivateRequest)}this._monitor=new h.ActivityMonitor({signal:this._context.model.contentChanged,timeout:e.renderTimeout});this._monitor.activityStopped.connect(this.update,this);this._ready.resolve(undefined)})).catch((e=>{requestAnimationFrame((()=>{this.dispose()}));void(0,o.showErrorMessage)(this._trans.__("Renderer Failure: %1",this._context.path),e)}))}[o.Printing.symbol](){return o.Printing.getPrintFunction(this.renderer)}get ready(){return this._ready.promise}setFragment(e){this._fragment=e;this.update()}dispose(){if(this.isDisposed){return}if(this._monitor){this._monitor.dispose()}this._monitor=null;super.dispose()}onUpdateRequest(e){if(this._context.isReady){void this._render();this._fragment=""}}async _render(){if(this.isDisposed){return}if(this._isRendering){this._renderRequested=true;return}this._renderRequested=false;const e=this._context;const t=e.model;const i={};if(this._dataType==="string"){i[this.mimeType]=t.toString()}else{i[this.mimeType]=t.toJSON()}const s=new l.MimeModel({data:i,callback:this._changeCallback,metadata:{fragment:this._fragment}});try{this._isRendering=true;await this.renderer.renderModel(s);this._isRendering=false;if(this._renderRequested){return this._render()}}catch(n){requestAnimationFrame((()=>{this.dispose()}));void(0,o.showErrorMessage)(this._trans.__("Renderer Failure: %1",e.path),n)}}}class T extends w{setFragment(e){this.content.setFragment(e)}}class C extends F{constructor(e){super(D.createRegistryOptions(e));this._rendermime=e.rendermime;this._renderTimeout=e.renderTimeout||1e3;this._dataType=e.dataType||"string";this._fileType=e.primaryFileType}createNewWidget(e){var t,i;const s=this._fileType;const n=(s===null||s===void 0?void 0:s.mimeTypes.length)?s.mimeTypes[0]:"text/plain";const a=this._rendermime.clone({resolver:e.urlResolver});const r=a.createRenderer(n);const o=new b({context:e,renderer:r,mimeType:n,renderTimeout:this._renderTimeout,dataType:this._dataType});o.title.icon=s===null||s===void 0?void 0:s.icon;o.title.iconClass=(t=s===null||s===void 0?void 0:s.iconClass)!==null&&t!==void 0?t:"";o.title.iconLabel=(i=s===null||s===void 0?void 0:s.iconLabel)!==null&&i!==void 0?i:"";const h=new T({content:o,context:e});return h}}var D;(function(e){function t(e){return Object.assign(Object.assign({},e),{readOnly:true})}e.createRegistryOptions=t})(D||(D={}));var O=i(17651);class S{constructor(e={}){this._modelFactories=Object.create(null);this._widgetFactories=Object.create(null);this._defaultWidgetFactory="";this._defaultWidgetFactoryOverrides=Object.create(null);this._defaultWidgetFactories=Object.create(null);this._defaultRenderedWidgetFactories=Object.create(null);this._widgetFactoriesForFileType=Object.create(null);this._fileTypes=[];this._extenders=Object.create(null);this._changed=new a.Signal(this);this._isDisposed=false;const t=e.textModelFactory;this.translator=e.translator||d.nullTranslator;if(t&&t.name!=="text"){throw new Error("Text model factory must have the name `text`")}this._modelFactories["text"]=t||new f;const i=e.initialFileTypes||S.getDefaultFileTypes(this.translator);i.forEach((e=>{const t=Object.assign(Object.assign({},S.getFileTypeDefaults(this.translator)),e);this._fileTypes.push(t)}))}get changed(){return this._changed}get isDisposed(){return this._isDisposed}dispose(){if(this.isDisposed){return}this._isDisposed=true;for(const e in this._modelFactories){this._modelFactories[e].dispose()}for(const e in this._widgetFactories){this._widgetFactories[e].dispose()}for(const e in this._extenders){this._extenders[e].length=0}this._fileTypes.length=0;a.Signal.clearData(this)}addWidgetFactory(e){const t=e.name.toLowerCase();if(!t||t==="default"){throw Error("Invalid factory name")}if(this._widgetFactories[t]){console.warn(`Duplicate registered factory ${t}`);return new n.DisposableDelegate(P.noOp)}this._widgetFactories[t]=e;for(const i of e.defaultFor||[]){if(e.fileTypes.indexOf(i)===-1){continue}if(i==="*"){this._defaultWidgetFactory=t}else{this._defaultWidgetFactories[i]=t}}for(const i of e.defaultRendered||[]){if(e.fileTypes.indexOf(i)===-1){continue}this._defaultRenderedWidgetFactories[i]=t}for(const i of e.fileTypes){if(!this._widgetFactoriesForFileType[i]){this._widgetFactoriesForFileType[i]=[]}this._widgetFactoriesForFileType[i].push(t)}this._changed.emit({type:"widgetFactory",name:t,change:"added"});return new n.DisposableDelegate((()=>{delete this._widgetFactories[t];if(this._defaultWidgetFactory===t){this._defaultWidgetFactory=""}for(const e of Object.keys(this._defaultWidgetFactories)){if(this._defaultWidgetFactories[e]===t){delete this._defaultWidgetFactories[e]}}for(const e of Object.keys(this._defaultRenderedWidgetFactories)){if(this._defaultRenderedWidgetFactories[e]===t){delete this._defaultRenderedWidgetFactories[e]}}for(const e of Object.keys(this._widgetFactoriesForFileType)){m.ArrayExt.removeFirstOf(this._widgetFactoriesForFileType[e],t);if(this._widgetFactoriesForFileType[e].length===0){delete this._widgetFactoriesForFileType[e]}}for(const e of Object.keys(this._defaultWidgetFactoryOverrides)){if(this._defaultWidgetFactoryOverrides[e]===t){delete this._defaultWidgetFactoryOverrides[e]}}this._changed.emit({type:"widgetFactory",name:t,change:"removed"})}))}addModelFactory(e){const t=e.name.toLowerCase();if(this._modelFactories[t]){console.warn(`Duplicate registered factory ${t}`);return new n.DisposableDelegate(P.noOp)}this._modelFactories[t]=e;this._changed.emit({type:"modelFactory",name:t,change:"added"});return new n.DisposableDelegate((()=>{delete this._modelFactories[t];this._changed.emit({type:"modelFactory",name:t,change:"removed"})}))}addWidgetExtension(e,t){e=e.toLowerCase();if(!(e in this._extenders)){this._extenders[e]=[]}const i=this._extenders[e];const s=m.ArrayExt.firstIndexOf(i,t);if(s!==-1){console.warn(`Duplicate registered extension for ${e}`);return new n.DisposableDelegate(P.noOp)}this._extenders[e].push(t);this._changed.emit({type:"widgetExtension",name:e,change:"added"});return new n.DisposableDelegate((()=>{m.ArrayExt.removeFirstOf(this._extenders[e],t);this._changed.emit({type:"widgetExtension",name:e,change:"removed"})}))}addFileType(e){const t=Object.assign(Object.assign(Object.assign({},S.getFileTypeDefaults(this.translator)),e),!(e.icon||e.iconClass)&&{icon:O.fileIcon});this._fileTypes.push(t);this._changed.emit({type:"fileType",name:t.name,change:"added"});return new n.DisposableDelegate((()=>{m.ArrayExt.removeFirstOf(this._fileTypes,t);this._changed.emit({type:"fileType",name:e.name,change:"removed"})}))}preferredWidgetFactories(e){const t=new Set;const i=this.getFileTypesForPath(h.PathExt.basename(e));i.forEach((e=>{if(e.name in this._defaultWidgetFactoryOverrides){t.add(this._defaultWidgetFactoryOverrides[e.name])}}));i.forEach((e=>{if(e.name in this._defaultWidgetFactories){t.add(this._defaultWidgetFactories[e.name])}}));i.forEach((e=>{if(e.name in this._defaultRenderedWidgetFactories){t.add(this._defaultRenderedWidgetFactories[e.name])}}));if(this._defaultWidgetFactory){t.add(this._defaultWidgetFactory)}i.forEach((e=>{if(e.name in this._widgetFactoriesForFileType){(0,m.each)(this._widgetFactoriesForFileType[e.name],(e=>{t.add(e)}))}}));if("*"in this._widgetFactoriesForFileType){(0,m.each)(this._widgetFactoriesForFileType["*"],(e=>{t.add(e)}))}const s=[];t.forEach((e=>{const t=this._widgetFactories[e];if(!t){return}const i=t.modelName||"text";if(i in this._modelFactories){s.push(t)}}));return s}defaultRenderedWidgetFactory(e){const t=this.getFileTypesForPath(h.PathExt.basename(e));let i=undefined;for(const s of t){if(s.name in this._defaultRenderedWidgetFactories){i=this._widgetFactories[this._defaultRenderedWidgetFactories[s.name]];break}}return i||this.defaultWidgetFactory(e)}defaultWidgetFactory(e){if(!e){return this._widgetFactories[this._defaultWidgetFactory]}return this.preferredWidgetFactories(e)[0]}setDefaultWidgetFactory(e,t){e=e.toLowerCase();if(!this.getFileType(e)){throw Error(`Cannot find file type ${e}`)}if(!t){if(this._defaultWidgetFactoryOverrides[e]){delete this._defaultWidgetFactoryOverrides[e]}return}if(!this.getWidgetFactory(t)){throw Error(`Cannot find widget factory ${t}`)}t=t.toLowerCase();const i=this._widgetFactoriesForFileType[e];if(t!==this._defaultWidgetFactory&&!(i&&i.includes(t))){throw Error(`Factory ${t} cannot view file type ${e}`)}this._defaultWidgetFactoryOverrides[e]=t}widgetFactories(){return(0,m.map)(Object.keys(this._widgetFactories),(e=>this._widgetFactories[e]))}modelFactories(){return(0,m.map)(Object.keys(this._modelFactories),(e=>this._modelFactories[e]))}widgetExtensions(e){e=e.toLowerCase();if(!(e in this._extenders)){return(0,m.empty)()}return new m.ArrayIterator(this._extenders[e])}fileTypes(){return new m.ArrayIterator(this._fileTypes)}getWidgetFactory(e){return this._widgetFactories[e.toLowerCase()]}getModelFactory(e){return this._modelFactories[e.toLowerCase()]}getFileType(e){e=e.toLowerCase();return(0,m.find)(this._fileTypes,(t=>t.name.toLowerCase()===e))}getKernelPreference(e,t,i){t=t.toLowerCase();const s=this._widgetFactories[t];if(!s){return void 0}const n=this.getModelFactory(s.modelName||"text");if(!n){return void 0}const a=n.preferredLanguage(h.PathExt.basename(e));const r=i&&i.name;const o=i&&i.id;return{id:o,name:r,language:a,shouldStart:s.preferKernel,canStart:s.canStartKernel,shutdownOnDispose:s.shutdownOnClose}}getFileTypeForModel(e){switch(e.type){case"directory":return(0,m.find)(this._fileTypes,(e=>e.contentType==="directory"))||S.getDefaultDirectoryFileType(this.translator);case"notebook":return(0,m.find)(this._fileTypes,(e=>e.contentType==="notebook"))||S.getDefaultNotebookFileType(this.translator);default:if(e.name||e.path){const t=e.name||h.PathExt.basename(e.path);const i=this.getFileTypesForPath(t);if(i.length>0){return i[0]}}return this.getFileType("text")||S.getDefaultTextFileType(this.translator)}}getFileTypesForPath(e){const t=[];const i=h.PathExt.basename(e);let s=(0,m.find)(this._fileTypes,(e=>!!(e.pattern&&e.pattern.match(i)!==null)));if(s){t.push(s)}let n=P.extname(i);while(n.length>1){s=(0,m.find)(this._fileTypes,(e=>e.extensions.indexOf(n)!==-1));if(s){t.push(s)}n="."+n.split(".").slice(2).join(".")}return t}}(function(e){function t(e){e=e||d.nullTranslator;const t=e===null||e===void 0?void 0:e.load("jupyterlab");return{name:"default",displayName:t.__("default"),extensions:[],mimeTypes:[],contentType:"file",fileFormat:"text"}}e.getFileTypeDefaults=t;function i(e){e=e||d.nullTranslator;const i=e===null||e===void 0?void 0:e.load("jupyterlab");const s=t(e);return Object.assign(Object.assign({},s),{name:"text",displayName:i.__("Text"),mimeTypes:["text/plain"],extensions:[".txt"],icon:O.fileIcon})}e.getDefaultTextFileType=i;function s(e){e=e||d.nullTranslator;const i=e===null||e===void 0?void 0:e.load("jupyterlab");return Object.assign(Object.assign({},t(e)),{name:"notebook",displayName:i.__("Notebook"),mimeTypes:["application/x-ipynb+json"],extensions:[".ipynb"],contentType:"notebook",fileFormat:"json",icon:O.notebookIcon})}e.getDefaultNotebookFileType=s;function n(e){e=e||d.nullTranslator;const i=e===null||e===void 0?void 0:e.load("jupyterlab");return Object.assign(Object.assign({},t(e)),{name:"directory",displayName:i.__("Directory"),extensions:[],mimeTypes:["text/directory"],contentType:"directory",icon:O.folderIcon})}e.getDefaultDirectoryFileType=n;function a(e){e=e||d.nullTranslator;const t=e===null||e===void 0?void 0:e.load("jupyterlab");return[i(e),s(e),n(e),{name:"markdown",displayName:t.__("Markdown File"),extensions:[".md"],mimeTypes:["text/markdown"],icon:O.markdownIcon},{name:"pdf",displayName:t.__("PDF File"),extensions:[".pdf"],mimeTypes:["application/pdf"],icon:O.pdfIcon},{name:"python",displayName:t.__("Python File"),extensions:[".py"],mimeTypes:["text/x-python"],icon:O.pythonIcon},{name:"json",displayName:t.__("JSON File"),extensions:[".json"],mimeTypes:["application/json"],icon:O.jsonIcon},{name:"csv",displayName:t.__("CSV File"),extensions:[".csv"],mimeTypes:["text/csv"],icon:O.spreadsheetIcon},{name:"tsv",displayName:t.__("TSV File"),extensions:[".tsv"],mimeTypes:["text/csv"],icon:O.spreadsheetIcon},{name:"r",displayName:t.__("R File"),mimeTypes:["text/x-rsrc"],extensions:[".r"],icon:O.rKernelIcon},{name:"yaml",displayName:t.__("YAML File"),mimeTypes:["text/x-yaml","text/yaml"],extensions:[".yaml",".yml"],icon:O.yamlIcon},{name:"svg",displayName:t.__("Image"),mimeTypes:["image/svg+xml"],extensions:[".svg"],icon:O.imageIcon,fileFormat:"base64"},{name:"tiff",displayName:t.__("Image"),mimeTypes:["image/tiff"],extensions:[".tif",".tiff"],icon:O.imageIcon,fileFormat:"base64"},{name:"jpeg",displayName:t.__("Image"),mimeTypes:["image/jpeg"],extensions:[".jpg",".jpeg"],icon:O.imageIcon,fileFormat:"base64"},{name:"gif",displayName:t.__("Image"),mimeTypes:["image/gif"],extensions:[".gif"],icon:O.imageIcon,fileFormat:"base64"},{name:"png",displayName:t.__("Image"),mimeTypes:["image/png"],extensions:[".png"],icon:O.imageIcon,fileFormat:"base64"},{name:"bmp",displayName:t.__("Image"),mimeTypes:["image/bmp"],extensions:[".bmp"],icon:O.imageIcon,fileFormat:"base64"}]}e.getDefaultFileTypes=a})(S||(S={}));var P;(function(e){function t(e){const t=h.PathExt.basename(e).split(".");t.shift();const i="."+t.join(".");return i.toLowerCase()}e.extname=t;function i(){}e.noOp=i})(P||(P={}))}}]);