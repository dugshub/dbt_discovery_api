## **FastAPI Endpoint Implementation and Higher Level Abstraction Layer**

The existing project provides a foundation for interacting with the dbt Cloud API and provides a set of services for working with dbt Cloud resources. 
The discoveryAPI interface currently provides 2 levels of abstraction, the first (service layer) and the second (api layer). 
The service layer provides a low-level interface to the dbt Cloud GraphQL API through API, while the api layer provides a higher-level interface to the service layer.

We will be adding a third (client layer) that will provide a higher-level interface on top of the API layer with more user-friendly types and methods. This will be exposed as a REST API as well as an AI Agent Toolset.


## **Overview**

Create a reporting focused abstraction utilizing the existing dbt_api in /src that will act as a standalone client for all of the dbt API endpoints. This service will run as a FastAPI application exposing a REST API and an AI Agent Toolset.


## **Project Structure and Architecture**

### **Directory Structure**

```
src/[PROJECT_NAME]/
├── client/
│   ├── __init__.py
│   └── [client_implementation].py      # Describe client responsibilities
├── models/                             # Pydantic models
│   ├── __init__.py
│   ├── base.py                         # Base/common models
│   └── [resource_models].py            # Resource-specific models
├── queries/                            # GraphQL or other query definitions
│   ├── __init__.py
│   └── [resource_queries].py           # Resource-specific queries
├── services/                           # Service layer implementations
│   ├── __init__.py
│   └── [resource_service].py           # Resource-specific services
├── api/                                # Public API layer
│   ├── __init__.py                     # Public exports
│   ├── [context].py                    # API context
│   └── resources/                      # Resource classes
│       ├── __init__.py
│       ├── base.py                     # Base resource class
│       └── [resource].py               # Resource-specific classes
└── exceptions.py                       # Custom exception types
```

[Adjust directory structure based on project needs. Include comments explaining the purpose of each directory and key file.]

### **Core Architecture**

1. **[Architecture Pattern]**
    - [Describe layer 1]: Responsibilities and boundaries
    - [Describe layer 2]: Responsibilities and boundaries
    - [Describe layer 3]: Responsibilities and boundaries

2. **Data Flow**

[Describe or provide a diagram showing how data flows through the system. Include key components and their interactions.]

3. **Key Principles**
    - [Principle 1]: Description and importance
    - [Principle 2]: Description and importance
    - [Principle 3]: Description and importance

[The architecture section should establish clear patterns for implementation, focusing on separation of concerns, consistent interfaces, and proper abstraction.]

## **Implementation Phases**

### Starting Context (This section can be added as needed across the implementation below. it is encouraged to add a section for each major phase of the implementation to appropriately manage context)

- [read-only or add] [relative_file_path_from_root]
- [add] [relative_file_path_from_root_of_new_file] (new file)

### Ending Context

- [read-only or add] [relative_file_path_from_root]
- [add] [relative_file_path_from_root_of_new_file] (new file)

### **Phase 1: [Core Infrastructure]**

1. **[Component 1]**

```python
# [file_path]
"""[Module description]"""

[Import statements]

class [Class]:
    """[Class description]"""

    def __init__(self, [params]):
        """[Method description]

        Args:
            [param]: [description]
        """
        pass

    def [method_name](self, [params]) -> [return_type]:
        """[Method description]

        Args:
            [param]: [description]

        Returns:
            [description]
        """
        pass
```

[Provide skeleton implementations with docstrings and type hints for key components. Focus on defining interfaces rather than implementations.]

### **Phase 2: [Component Implementation]**

[Continue with additional phases and components as needed]

## **Dependencies**

```
# requirements.txt
[dependency]>=[version]
[dependency]>=[version]
[dependency]>=[version]
```

[List all external dependencies with version requirements. Include comments explaining why each dependency is needed.]

## **Configuration**

```
# .env.example
[CONFIG_VARIABLE]=value
[CONFIG_VARIABLE]=value
```

[Document required configuration variables, their purpose, and example values.]

## **Usage Example**

```python
# Example usage of the library
from [project] import [components]

# Example implementation goes here
```

[Provide skeleton examples of how the library will be used by clients. Focus on the public API interface.]

## **Success Criteria**

1. **Functionality**
    - [Criterion 1]
    - [Criterion 2]
    - [Criterion 3]

2. **Usability**
    - [Criterion 1]
    - [Criterion 2]
    - [Criterion 3]

3. **Quality**
    - [Criterion 1]
    - [Criterion 2]
    - [Criterion 3]

[Define clear, measurable criteria for what makes this MVP successful. These should align with project goals and user needs.]

## **Timeline**

- **Phase 1**: [Description and timeline]
- **Phase 2**: [Description and timeline]
- **Phase 3**: [Description and timeline]
- **Phase 4**: [Description and timeline]

[Outline the implementation phases with rough timelines or priorities.]

## **Next Steps After MVP**

1. **[Future Area 1]**
    - [Feature/enhancement]
    - [Feature/enhancement]
    
2. **[Future Area 2]**
    - [Feature/enhancement]
    - [Feature/enhancement]

3. **[Future Area 3]**
    - [Feature/enhancement]
    - [Feature/enhancement]

[Document potential future enhancements and features that are deliberately out of scope for the MVP but may be considered in future iterations.]

## **Implementation Notes**

[Include any additional guidance for implementers. This might include:
- Architectural decisions and their rationales
- Patterns to follow or avoid
- Performance considerations
- Testing approaches
- Security considerations]

---

### **Template Completion Guide**

When filling in this template:
1. Replace bracketed text with actual content
2. Maintain consistent style and formatting
3. Include comprehensive docstrings and type hints
4. Focus on interfaces rather than implementations
5. Ensure all success criteria are measurable
6. Be explicit about what's in and out of scope
7. Consider dependencies and their implications
