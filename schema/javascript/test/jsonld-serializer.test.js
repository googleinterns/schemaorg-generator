const expect = require('chai').expect;
const schema = require("./schema_pb");
const schemaDescriptor = require("./schema_descriptor.json");
const JSONLDSerializer = require("../index").JSONLDSerializer;

// Test serialization of date.
//     Procedure:
//         - Create a new serializer.
//         - Create a date object in proto.
//         - Set values for year, month and day.
//         - Make the expected output string in ISO8601 format.
//         - Call the proto_to_dict function of serializer along with schema and date object.
    
//     Verification:
//         - Check if the returned string is equal to expected string and is in ISO8601 format.
describe("Test Serialization of Date", () => {
    it("Testing serialization of Date.", () => {
        let serializer = new JSONLDSerializer();
        dt = new schema.Date();
        dt.setYear(2000);
        dt.setMonth(2);
        dt.setDay(9);
    
        let expected = "2000-02-09";
        let output = serializer.protoToDict(dt, "Date", schemaDescriptor);
        expect(output).to.equal(expected);
    });
});

// Test serialization of time.
//     Procedure:
//         - Create a new serializer.
//         - Create a time object in proto for following cases. 
//             * Without timezone.
//             * With timezone.
//         - Set values for hours, minutes and seconds.
//         - Make the expected output string for both cases in ISO8601 format.
//         - Call the proto_to_dict function of serializer along with schema and time object for both cases.
    
//     Verification:
//         - Check if the returned string is equal to expected string and is in ISO8601 format.
//         - Check if the timezone is added correctly.
describe("Test serialization of Time", () => {
    it("Testing serialization of time without timezone.", () => {
        let serializer = new JSONLDSerializer();
        tm = new schema.Time();
        tm.setHours(6);
        tm.setMinutes(30);
        tm.setSeconds(15);
    
        let expected = "06:30:15";
        let output = serializer.protoToDict(tm, "Time", schemaDescriptor);
        expect(output).to.equal(expected);
    });

    it("Testing serialization of time with timezone.", () => {
        let serializer = new JSONLDSerializer();
        tm = new schema.Time();
        tm.setHours(6);
        tm.setMinutes(30);
        tm.setSeconds(15);
        tm.setTimezone("+05:30");
    
        let expected = "06:30:15+05:30";
        let output = serializer.protoToDict(tm, "Time", schemaDescriptor);
        expect(output).to.equal(expected);
    });
});

// Test serialization of datetime.
//     Procedure:
//         - Create a new serializer.
//         - Create a datetime object in proto for following cases. 
//             * Without timezone.
//             * With timezone.
//         - Set values for hours, minutes and seconds.
//         - Set values for year, month and day.
//         - Make the expected output string for both cases in ISO8601 format.
//         - Call the proto_to_dict function of serializer along with schema and datetime object for both cases.
    
//     Verification:
//         - Check if the returned string is equal to expected string and is in ISO8601 format.
//         - Check if the timezone is added correctly.
describe("Test serialization of DateTime", () => {
    it("Testing serialization of datetime without timezone.", () => {
        let serializer = new JSONLDSerializer();
        
        dt = new schema.Date();
        dt.setYear(2000);
        dt.setMonth(2);
        dt.setDay(9);

        tm = new schema.Time();
        tm.setHours(6);
        tm.setMinutes(30);
        tm.setSeconds(15);

        dtt = new schema.DateTime();
        dtt.setDate(dt);
        dtt.setTime(tm);
    
        let expected = "2000-02-09T06:30:15";
        let output = serializer.protoToDict(dtt, "DateTime", schemaDescriptor);
        expect(output).to.equal(expected);
    });

    it("Testing serialization of datetime with timezone.", () => {
        let serializer = new JSONLDSerializer();
        
        dt = new schema.Date();
        dt.setYear(2000);
        dt.setMonth(2);
        dt.setDay(9);

        tm = new schema.Time();
        tm.setHours(6);
        tm.setMinutes(30);
        tm.setSeconds(15);
        tm.setTimezone("+05:30");

        dtt = new schema.DateTime();
        dtt.setDate(dt);
        dtt.setTime(tm);
    
        let expected = "2000-02-09T06:30:15+05:30";
        let output = serializer.protoToDict(dtt, "DateTime", schemaDescriptor);
        expect(output).to.equal(expected);
    });
});

// Test serialization of duration.
//     Procedure:
//         - Create a new serializer.
//         - Create a duration object in proto
//         - Set value for seconds.
//         - Make the expected output string in ISO8601 duration format.
//         - Call the proto_to_dict function of serializer along with schema and duration object.
    
//     Verification:
//         - Check if the returned string is equal to expected string and is in ISO8601 duration format.
describe("Test Serialization of Duration", () => {
    it("Testing serialization of Duration.", () => {
        let serializer = new JSONLDSerializer();
        dn = new schema.Duration();
        dn.setSeconds(100456123);
    
        let expected = "PT27904H28M43S";
        let output = serializer.protoToDict(dn, "Duration", schemaDescriptor);
        expect(output).to.equal(expected);
    });
});

// Test serialization of quantitative values.
//     Procedure:
//         - Create a new serializer.
//         - Create object of following types in proto:
//             * Mass
//             * Distance
//             * Energy
//         - Set the fields unit and value for each of the objects.
//         - Make the expected output string for each object.
//         - Call the proto_to_dict function of serializer along with schema and each object.
    
//     Verification:
//         - Check if the returned string is equal to '<value> <unit>' for each object.
describe("Test Serialization of Quantitative Values", () => {
    
    it("Testing serialization of Mass.", () => {
        let serializer = new JSONLDSerializer();
        ms = new schema.Mass();
        ms.setValue(10.5);
        ms.setUnit("KG");
    
        let expected = "10.5 KG";
        let output = serializer.protoToDict(ms, "Mass", schemaDescriptor);
        expect(output).to.equal(expected);
    });

    it("Testing serialization of Distance.", () => {
        let serializer = new JSONLDSerializer();
        ds = new schema.Distance();
        ds.setValue(10.5);
        ds.setUnit("Metre");
    
        let expected = "10.5 Metre";
        let output = serializer.protoToDict(ds, "Distance", schemaDescriptor);
        expect(output).to.equal(expected);
    });

    it("Testing serialization of Energy.", () => {
        let serializer = new JSONLDSerializer();
        eg = new schema.Energy();
        eg.setValue(10.5);
        eg.setUnit("Joules");
    
        let expected = "10.5 Joules";
        let output = serializer.protoToDict(eg, "Energy", schemaDescriptor);
        expect(output).to.equal(expected);
    });
});

// Test serialization of property.
//     Procedure:
//         - Create a new serializer.
//         - Create a proto property.
//         - Set any two fields of the property.
//         - Call the proto_to_dict function of serializer along with schema and property.
    
//     Verification:
//         - Check if the returned value is that of field set at last and that it is not enclosed inside any dict.
describe("Test Serialization of Property", () => {
    it("Testing serialization of Property.", () => {
        let serializer = new JSONLDSerializer();
        prop = new schema.PositionProperty();
        prop.setText("abc");
        prop.setUrl("def");
    
        let expected = "def";
        let output = serializer.protoToDict(prop, "position", schemaDescriptor);
        expect(output).to.equal(expected);
    });
});

// Test serialization of class.
//     Procedure:
//         - Create a new serializer.
//         - Create a proto class.
//         - Set two properties such that:
//             * It has a single value.
//             * It has multiple values.
//         - Set id for the class.
//         - Call the proto_to_dict function of serializer along with schema and class.
    
//     Verification:
//         - Check if the returned value is an python dict.
//         - Check if the property having single value is not enclosed in an an array/list.
//         - Check if the property having multiple values is enclosed inside an array.
//         - Check if the dict has '@type' key with value as schemaorg name of class.
//         - Check if the dict has '@id' field set to the id of class.
describe("Test Serialization of Class", () => {
    it("Testing serialization of Class.", () => {
        let serializer = new JSONLDSerializer();
        cls = new schema.Movie();
        cls.setId("test id 1");
        
        let name = new schema.NameProperty()
        name.setText("Name 1")
        cls.addName(name);

        let url1 = new schema.UrlProperty();
        url1.setUrl("URL 1");
        let url2 = new schema.UrlProperty();
        url2.setUrl("URL 2");

        cls.addUrl(url1);
        cls.addUrl(url2);
    
        let expected = {
            "@id": "test id 1",
            "@type": "Movie",
            "name": "Name 1",
            "url": [
                "URL 1",
                "URL 2"
                ]
        };

        let output = serializer.protoToDict(cls, "Movie", schemaDescriptor);
        expect(output).to.eql(expected);
    });
});

// Test serialization of enumeration.
//     Procedure:
//         - Create a new serializer.
//         - Create proto enumeration such it behaves as:
//             * Enumeration of multiple values.
//             * Class
//         - Set the value for the enumeration that behaves like enumeration of values.
//         - Set a property for the enumeration that behaves like a class.
//         - Set a id for the enumeration that behaves like a class.
//         - Call the proto_to_dict function of serializer along with each of the enumeration.
    
//     Verification:
//         - For enumeration that behaves like a enumeration of values check if returned value is a string pointing to its schema.org url.
//         - For enumeration that behaves as a class do the following:
//             * Check if the returned value is an python dict.
//             * Check if the property is populated.
//             * Check if the dict has '@type' key with value as schemaorg name of enumeration.
//             * Check if the dict has '@id' field set to the id of enumeration.
describe("Test Serialization of Enumeration", () => {
    it("Testing serialization of Enumeration(as enumeration of values).", () => {
        let serializer = new JSONLDSerializer();
        let rsvp = new schema.RsvpResponseType();
        rsvp.setId(schema.RsvpResponseTypeClass.Id["RSVP_RESPONSE_YES"]);
    
        let expected = "http://schema.org/RsvpResponseYes";

        let output = serializer.protoToDict(rsvp, "RsvpResponseType", schemaDescriptor);
        expect(output).to.equal(expected);
    });

    it("Testing serialization of Enumeration(as class).", () => {
        let serializer = new JSONLDSerializer();
        let rsvp = new schema.RsvpResponseType();
        let cls = new schema.RsvpResponseTypeClass();

        cls.setId("test id 1");
        let alname = new schema.AlternateNameProperty();
        alname.setText("Alternate Name 1");
        cls.addAlternateName(alname);

        rsvp.setRsvpResponseType(cls);
    
        let expected = {
            "@id": "test id 1",
            "@type": "RsvpResponseType",
            "alternateName": "Alternate Name 1"
        };

        let output = serializer.protoToDict(rsvp, "RsvpResponseType", schemaDescriptor);
        expect(output).to.eql(expected);
    });
});
