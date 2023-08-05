(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[7607,3469],{33469:(t,e,s)=>{"use strict";s.r(e);s.d(e,{AddWidget:()=>d,TagTool:()=>h,TagWidget:()=>r});var i=s(86992);var a=s(17651);var n=s(93144);class d extends i.Widget{constructor(t){super();this.parent=null;this.input=document.createElement("input");this.translator=t||n.nullTranslator;this._trans=this.translator.load("jupyterlab");this.addClass("tag");this.editing=false;this.buildTag()}buildTag(){const t=this.input||document.createElement("input");t.value=this._trans.__("Add Tag");t.contentEditable="true";t.className="add-tag";t.style.width="49px";this.input=t;const e=document.createElement("div");e.className="tag-holder";e.appendChild(t);const s=a.addIcon.element({tag:"span",elementPosition:"center",height:"18px",width:"18px",marginLeft:"3px",marginRight:"-5px"});this.addClass("unapplied-tag");e.appendChild(s);this.node.appendChild(e)}onAfterAttach(){this.node.addEventListener("mousedown",this);this.input.addEventListener("keydown",this);this.input.addEventListener("focus",this);this.input.addEventListener("blur",this)}onBeforeDetach(){this.node.removeEventListener("mousedown",this);this.input.removeEventListener("keydown",this);this.input.removeEventListener("focus",this);this.input.removeEventListener("blur",this)}handleEvent(t){switch(t.type){case"mousedown":this._evtMouseDown(t);break;case"keydown":this._evtKeyDown(t);break;case"blur":this._evtBlur();break;case"focus":this._evtFocus();break;default:break}}_evtMouseDown(t){if(!this.editing){this.editing=true;this.input.value="";this.input.focus()}else if(t.target!==this.input){if(this.input.value!==""){const t=this.input.value;this.parent.addTag(t);this.input.blur();this._evtBlur()}}t.preventDefault()}_evtFocus(){if(!this.editing){this.input.blur()}}_evtKeyDown(t){const e=document.createElement("span");e.className="add-tag";e.innerHTML=this.input.value;document.body.appendChild(e);this.input.style.width=e.getBoundingClientRect().width+8+"px";document.body.removeChild(e);if(t.keyCode===13){const t=this.input.value;this.parent.addTag(t);this.input.blur();this._evtBlur()}}_evtBlur(){if(this.editing){this.editing=false;this.input.value=this._trans.__("Add Tag");this.input.style.width="49px"}}}var l=s(93269);var o=s(28789);class r extends i.Widget{constructor(t){super();this.parent=null;this.applied=true;this.name=t;this.addClass("tag");this.buildTag()}buildTag(){const t=document.createElement("span");t.textContent=this.name;t.style.textOverflow="ellipsis";const e=document.createElement("div");e.className="tag-holder";e.appendChild(t);const s=a.checkIcon.element({tag:"span",elementPosition:"center",height:"18px",width:"18px",marginLeft:"5px",marginRight:"-3px"});if(this.applied){this.addClass("applied-tag")}else{this.addClass("unapplied-tag");s.style.display="none"}e.appendChild(s);this.node.appendChild(e)}onAfterAttach(){this.node.addEventListener("mousedown",this);this.node.addEventListener("mouseover",this);this.node.addEventListener("mouseout",this)}onBeforeDetach(){this.node.removeEventListener("mousedown",this);this.node.removeEventListener("mouseover",this);this.node.removeEventListener("mouseout",this)}handleEvent(t){switch(t.type){case"mousedown":this._evtClick();break;case"mouseover":this._evtMouseOver();break;case"mouseout":this._evtMouseOut();break;default:break}}onUpdateRequest(){var t;const e=(t=this.parent)===null||t===void 0?void 0:t.checkApplied(this.name);if(e!==this.applied){this.toggleApplied()}}toggleApplied(){var t,e;if(this.applied){this.removeClass("applied-tag");((t=this.node.firstChild)===null||t===void 0?void 0:t.lastChild).style.display="none";this.addClass("unapplied-tag")}else{this.removeClass("unapplied-tag");((e=this.node.firstChild)===null||e===void 0?void 0:e.lastChild).style.display="inline-block";this.addClass("applied-tag")}this.applied=!this.applied}_evtClick(){var t,e;if(this.applied){(t=this.parent)===null||t===void 0?void 0:t.removeTag(this.name)}else{(e=this.parent)===null||e===void 0?void 0:e.addTag(this.name)}this.toggleApplied()}_evtMouseOver(){this.node.classList.add("tag-hover")}_evtMouseOut(){this.node.classList.remove("tag-hover")}}class h extends o.NotebookTools.Tool{constructor(t,e,s){super();this.tagList=[];this.label=false;e;this.translator=s||n.nullTranslator;this._trans=this.translator.load("jupyterlab");this.tracker=t;this.layout=new i.PanelLayout;this.createTagInput();this.addClass("jp-TagTool")}createTagInput(){const t=this.layout;const e=new d(this.translator);e.id="add-tag";t.insertWidget(0,e)}checkApplied(t){var e;const s=(e=this.tracker)===null||e===void 0?void 0:e.activeCell;if(s){const e=s.model.metadata.get("tags");if(e){return e.includes(t)}}return false}addTag(t){var e;const s=(e=this.tracker)===null||e===void 0?void 0:e.activeCell;if(s){const e=s.model.metadata.get("tags")||[];let i=t.split(/[,\s]+/);i=i.filter((t=>t!==""&&!e.includes(t)));s.model.metadata.set("tags",e.concat(i));this.refreshTags();this.loadActiveTags()}}removeTag(t){var e;const s=(e=this.tracker)===null||e===void 0?void 0:e.activeCell;if(s){const e=s.model.metadata.get("tags");let i=e.filter((e=>e!==t));s.model.metadata.set("tags",i);if(i.length===0){s.model.metadata.delete("tags")}this.refreshTags();this.loadActiveTags()}}loadActiveTags(){const t=this.layout;for(const e of t.widgets){e.update()}}pullTags(){var t,e;const s=(t=this.tracker)===null||t===void 0?void 0:t.currentWidget;const i=((e=s===null||s===void 0?void 0:s.model)===null||e===void 0?void 0:e.cells)||[];const a=(0,l.reduce)(i,((t,e)=>{const s=e.metadata.get("tags")||[];return[...t,...s]}),[]);this.tagList=[...new Set(a)].filter((t=>t!==""))}refreshTags(){this.pullTags();const t=this.layout;const e=t.widgets.filter((t=>t.id!=="add-tag"));e.forEach((t=>{if(!this.tagList.includes(t.name)){t.dispose()}}));const s=e.map((t=>t.name));this.tagList.forEach((e=>{if(!s.includes(e)){const s=t.widgets.length-1;t.insertWidget(s,new r(e))}}))}validateTags(t,e){e=e.filter((t=>typeof t==="string"));e=(0,l.reduce)(e,((t,e)=>[...t,...e.split(/[,\s]+/)]),[]);const s=[...new Set(e)].filter((t=>t!==""));t.model.metadata.set("tags",s);this.refreshTags();this.loadActiveTags()}onActiveCellChanged(){this.loadActiveTags()}onAfterShow(){this.refreshTags();this.loadActiveTags()}onAfterAttach(){if(!this.label){const t=document.createElement("label");t.textContent=this._trans.__("Cell Tags");t.className="tag-label";this.parent.node.insertBefore(t,this.node);this.label=true}if(this.tracker.currentWidget){void this.tracker.currentWidget.context.ready.then((()=>{this.refreshTags();this.loadActiveTags()}));this.tracker.currentWidget.model.cells.changed.connect((()=>{this.refreshTags();this.loadActiveTags()}))}this.tracker.currentChanged.connect((()=>{this.refreshTags();this.loadActiveTags()}))}onActiveCellMetadataChanged(){const t=this.tracker.activeCell.model.metadata.get("tags");let e=[];if(t===undefined){return}if(typeof t==="string"){e.push(t)}else{e=t}this.validateTags(this.tracker.activeCell,e)}}}}]);