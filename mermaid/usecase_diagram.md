flowchart TB
    %% Actors
    User(("👤 User"))
    System(("⚙️ System"))
    Database[("🗄️ Database")]

    %% System Boundary
    subgraph Markdown to JSON System
        %% Primary Use Cases
        Convert["📄 Convert Markdown to JSON"]
        Validate["✅ Validate Document"]
        SaveDB["💾 Save to Database"]
        
        %% Validation Use Cases
        subgraph Validation System
            direction TB
            ValidateSchema["🔍 Schema Validation"]
            ValidateContent["📝 Content Validation"]
            ValidateStructure["🌳 Structure Validation"]
            FormatErrors["❌ Error Formatting"]
        end

        %% Database Use Cases
        subgraph Database Operations
            direction TB
            SaveDoc["📋 Save Document"]
            SaveSections["📑 Save Sections"]
            SaveJSON["🔄 Save JSON"]
            SaveValidation["📊 Save Results"]
        end
    end

    %% Relationships
    User --> Convert
    Convert --> Validate
    Validate --> ValidateSchema
    Validate --> ValidateContent
    Validate --> ValidateStructure
    ValidateSchema --> FormatErrors
    ValidateContent --> FormatErrors
    ValidateStructure --> FormatErrors
    
    Convert --> SaveDB
    SaveDB --> SaveDoc
    SaveDB --> SaveSections
    SaveDB --> SaveJSON
    SaveDB --> SaveValidation
    
    SaveDoc --> Database
    SaveSections --> Database
    SaveJSON --> Database
    SaveValidation --> Database
    
    %% Add descriptions using native styling
    Convert -. "1. Reads markdown file<br/>2. Parses content<br/>3. Generates JSON" .-> System
    Validate -. "1. Schema validation<br/>2. Content validation<br/>3. Structure validation" .-> System
    SaveDB -. "1. Document metadata<br/>2. Section hierarchy<br/>3. JSON output<br/>4. Validation results" .-> System
