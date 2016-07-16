//old relic file, for posterity


var primes = []
var number = {
	value : 1,
	prime : true
}

while (primes.length < 10001) {
	number.value ++;
	number.prime = true;
	number.sqrt = Math.sqrt(number.value);
	for (var i = 2; i <= number.sqrt; i++){
		if (number.value % i == 0) {
			number.prime = false;
		}
	}
	if (number.prime == true) {
		primes.push(number.value);
	}
}

console.log(primes[primes.length - 1]);
