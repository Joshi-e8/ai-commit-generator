/**
 * Test file 2 for multi-file commit testing.
 */

function functionTwo() {
    // This is a new function in file 2
    console.log("Function two called");
    return "Hello from file 2";
}

class TestClass2 {
    constructor() {
        this.name = "TestClass2";
    }
    
    getInfo() {
        return `This is ${this.name}`;
    }
}

export { functionTwo, TestClass2 };
