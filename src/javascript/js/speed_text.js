function test_reduce(a){
	var t1 = new Date().getTime();
	b = a.reduce(add);
	var t2 = new Date().getTime();
	return b;
}