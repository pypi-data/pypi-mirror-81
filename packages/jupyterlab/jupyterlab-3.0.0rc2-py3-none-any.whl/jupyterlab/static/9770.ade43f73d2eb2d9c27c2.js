(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[9770],{39770:(e,t,r)=>{"use strict";r.r(t);r.d(t,{AttachedProperty:()=>a});var a=function(){function e(e){this._pid=i.nextPID();this.name=e.name;this._create=e.create;this._coerce=e.coerce||null;this._compare=e.compare||null;this._changed=e.changed||null}e.prototype.get=function(e){var t;var r=i.ensureMap(e);if(this._pid in r){t=r[this._pid]}else{t=r[this._pid]=this._createValue(e)}return t};e.prototype.set=function(e,t){var r;var a=i.ensureMap(e);if(this._pid in a){r=a[this._pid]}else{r=a[this._pid]=this._createValue(e)}var n=this._coerceValue(e,t);this._maybeNotify(e,r,a[this._pid]=n)};e.prototype.coerce=function(e){var t;var r=i.ensureMap(e);if(this._pid in r){t=r[this._pid]}else{t=r[this._pid]=this._createValue(e)}var a=this._coerceValue(e,t);this._maybeNotify(e,t,r[this._pid]=a)};e.prototype._createValue=function(e){var t=this._create;return t(e)};e.prototype._coerceValue=function(e,t){var r=this._coerce;return r?r(e,t):t};e.prototype._compareValue=function(e,t){var r=this._compare;return r?r(e,t):e===t};e.prototype._maybeNotify=function(e,t,r){var a=this._changed;if(a&&!this._compareValue(t,r)){a(e,t,r)}};return e}();(function(e){function t(e){i.ownerData.delete(e)}e.clearData=t})(a||(a={}));var i;(function(e){e.ownerData=new WeakMap;e.nextPID=function(){var e=0;return function(){var t=Math.random();var r=(""+t).slice(2);return"pid-"+r+"-"+e++}}();function t(t){var r=e.ownerData.get(t);if(r){return r}r=Object.create(null);e.ownerData.set(t,r);return r}e.ensureMap=t})(i||(i={}))}}]);