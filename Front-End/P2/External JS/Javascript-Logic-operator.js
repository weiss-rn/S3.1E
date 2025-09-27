var me = 20;
var you = 10;

var correct = me > you;
var incorrect = me < you; 

var result = correct && incorrect;
console.log(result);
document.write('${correct} && ${incorrect} = ${result}<br/>');

var result = correct || incorrect;
console.log(result);
document.write('${correct} || ${incorrect} = ${result}<br/>');

var result = !incorrect;
console.log(result);
document.write('!${incorrect} = ${result}<br/>');
