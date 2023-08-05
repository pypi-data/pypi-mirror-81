from google.cloud import datacatalog_v1beta1

from datacatalog_tag_template_processor import constant


class DataCatalogEntityFactory:
    __TRUTHS = {1, '1', 't', 'T', 'true', 'True', 'TRUE'}

    @classmethod
    def make_tag_template(cls, tag_template_dict):
        tag_template = datacatalog_v1beta1.types.TagTemplate()

        tag_template.display_name = tag_template_dict['display_name']

        fields = tag_template_dict['fields']

        field_order = len(fields)
        for field_id, items in fields.items():
            field_display_name = items['field_display_name']
            field_type = items['field_type']

            tag_template.fields[field_id].display_name = field_display_name

            field_type = field_type.upper()

            if field_type in constant.ALLOWED_BOOL_VALUES:
                tag_template.fields[field_id].type.primitive_type = \
                    datacatalog_v1beta1.enums.FieldType.PrimitiveType.BOOL.value
            elif field_type in constant.ALLOWED_DOUBLE_VALUES:
                tag_template.fields[field_id].type.primitive_type = \
                    datacatalog_v1beta1.enums.FieldType.PrimitiveType.DOUBLE.value
            elif field_type in constant.ALLOWED_STRING_VALUES:
                tag_template.fields[field_id].type.primitive_type = \
                    datacatalog_v1beta1.enums.FieldType.PrimitiveType.STRING.value
            elif field_type in constant.ALLOWED_DATETIME_VALUES:
                tag_template.fields[field_id].type.primitive_type = \
                    datacatalog_v1beta1.enums.FieldType.PrimitiveType.TIMESTAMP.value
            elif field_type in constant.ALLOWED_ENUM_VALUES:
                enum_values = items['enum_values']
                for enum_value in enum_values:
                    tag_template.fields[field_id].type.enum_type \
                        .allowed_values.add().display_name = enum_value

            tag_template.fields[field_id].order = field_order
            field_order -= 1

        return tag_template
