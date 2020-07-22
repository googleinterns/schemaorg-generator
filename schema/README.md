# Schema

  

This directory contains protocol buffer format releases of different schemaorg schemas.

The schema releases are tied to the release version of the schema.org https://schema.org/docs/releases.html

 
These protocol buffers can be used to generate JSON-LD schema files in any supported language.

## Modelling Schema to Protobuf
### Datatypes

 - Text is modelled as a string.
 - URL is modelled as a string.
 - Number is modelled as a double.
 - Float is modelled as a double.
 - Integer is modelled as int64.
 - Boolean is modelled as a bool.
 - Date, Time and Datetime is modelled as below.
 
 ##### Date
 
```
    message  Date {
	    option (type) = "DatatypeDate";
	    int32  year = 1;
	    int32  month = 2;
	    int32  day = 3;
    }
```  

 ##### Time

```
    message  Time {
	    option (type) = "DatatypeTime";
	    int32  hours = 1;
	    int32  minutes = 2;
	    int32  seconds = 3;
	    Timezone  timezone = 4;
    }
```
 
   ##### DateTime
   
```
    message  DateTime {
	    option (type) = "DatatypeDateTime";
	    Date  date = 1;
	    Time  time = 2;
    }
```
   ##### Timezone
   
```
    message  Timezone {
	    string  iana_id = 1;
    }
```
 ##### Duration

```
    message  Duration {
	    option (type) = "DatatypeDuration";
	    int64 seconds = 1;
    }
```

 ##### Quantitative Values

```
    message  Mass {
	    option (type) = "DatatypeQuantitative";
	    double value = 1;
		string unit = 2;
    }
	
	message  Energy {
	    option (type) = "DatatypeQuantitative";
	    double value = 1;
		string unit = 2;
    }

	message  Distance {
	    option (type) = "DatatypeQuantitative";
	    double value = 1;
		string unit = 2;
    }
```

### Properties

 Properties are modelled as *message* which consist of a single *oneof* consisting of all the possible values of property mapped using [[https://schema.org/rangeIncludes](https://schema.org/rangeIncludes)].

 All the parent classes of any class in the *rangeIncludes* of the property is also included in the property to model the inheritance heirarchy.

#### Example
The property countryOfOrigin has its range in :

 - AdministrativeArea
 - Country
 - Place
 - Thing

countryOfOrigin is modelled as :

```
    message  CountryOfOriginProperty {
	    option (type) = "Property";
	    oneof values {
		    AdministrativeArea  administrative_area = 1;
		    Country  country = 2;
		    Place  place = 3;
		    Thing  thing = 4;
	    }
    }
```
 

### Classes

  Classes that are not *subTypeOf* enumeration are modelled as a *message*
   with each property that is mapped to it using [[https://schema.org/domainIncludes](https://schema.org/domainIncludes)] being added as as a *repeated* field  in the message description.

   Classes also includes the property that belongs to any of the parent classes of the class. The parent class relationship is identified using [[http://www.w3.org/2000/01/rdf-schema#subClassOf ](http://www.w3.org/2000/01/rdf-schema#subClassOf)].


#### Example
Considering first 5 properties of the class AMRadioChannel:
##### Properties

 - additionalType
 - alternateName
 - broadcastChannelId
 - broadcastFrequency
 - broadcastServiceTier

AMRadioChannel is modelled as:
```
    message  AMRadioChannel {
	    option (type) = "AMRadioChannel";
	    repeated  AdditionalTypeProperty  additional_type = 1 [json_name="additionalType"];
	    repeated  AlternateNameProperty  alternate_name = 2 [json_name="alternateName"];
	    repeated  BroadcastChannelIdProperty  broadcast_channel_id = 3 [json_name="broadcastChannelId"];
	    repeated  BroadcastFrequencyProperty  broadcast_frequency = 4 [json_name="broadcastFrequency"];
	    repeated  BroadcastServiceTierProperty  broadcast_service_tier = 5 [json_name="broadcastServiceTier"];
	}
```
### Enumerations
Enumerations are identified using [**[http://www.w3.org/2000/01/rdf-schema#subClassOf](http://www.w3.org/2000/01/rdf-schema#subClassOf)**] predicate. 

All the enumerations also behave as class having properties attached to it. So, enumerations are modelled as oneof of two messages:

1. The enum values themselves.
2. The class with the properties.


#### Example
Consider the enumeration GamePlayMode.
##### Enum Values

 - CoOp
 - MultiPlayer
 - SinglePlayer
 
 ##### Properties (First 5)
 
 - additionalType
 - alternateName
 - description
 - disambiguatingDescription
 - identifier
 
 GamePlayMode is modelled as:
 
```
    message  GamePlayMode {
	    option (type) = "EnumWrapper";
	    oneof values {
		    GamePlayModeImpl.Id  id = 1;
		    GamePlayModeImpl  game_play_mode = 2;
	    }
    }
    
    message  GamePlayModeClass {
	    option (type) = "GamePlayMode";
	    enum  Id {
		    UNKNOWN = 0 [(schemaorg_value)="Unknown"];
		    CO_OP = 1 [(schemaorg_value)="https://schema.org/CoOp"];
		    MULTI_PLAYER = 2 [(schemaorg_value)="https://schema.org/MultiPlayer"];
		    SINGLE_PLAYER = 3 [(schemaorg_value)="https://schema.org/SinglePlayer"];
	    }
    
	    repeated  AdditionalTypeProperty  additional_type = 1 [json_name="additionalType"];
	    repeated  AlternateNameProperty  alternate_name = 2 [json_name="alternateName"];
	    repeated  DescriptionProperty  description = 3 [json_name="description"];
	    repeated  DisambiguatingDescriptionProperty  disambiguating_description = 4 [json_name="disambiguatingDescription"];
	    repeated  IdentifierProperty  identifier = 5 [json_name="identifier"];
    }
    
```
 