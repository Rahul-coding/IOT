
import oci
import os
import uuid
import base64
import sys

sys.path.append('../')
config = {
    "user": os.getenv('OCI_USER'),
    "key_content": os.getenv('OCI_KEY'),
    "fingerprint": os.getenv('OCI_KEY_FINGERPRINT'),
    "tenancy": os.getenv('OCI_TENANCY'),
    "region": os.getenv('OCI_REGION')
}

# Compartment where processor job will be created
COMPARTMENT_ID = "ocid1.compartment.oc1..aaaaaaaac3cxhzoka75zaaysugzmvhm3ni3keqvikawjxvwpz26mud622owa"  # e.g. "ocid1.compartment.oc1..aaaaaaaae5j73axsja5fnahbn23ilop3ynjkcg77mcvgryddz4pkh2t5ppaq";

def create_processor_job_callback(times_called, response):
    print("Waiting for processor lifecycle state to go into succeeded state:", response.data)
def analyze(image):
    text_extraction_sample_string = None
    with open(image, "rb") as document_file:
        text_extraction_sample_string = base64.b64encode(document_file.read()).decode('utf-8')

    aiservicedocument_client = oci.ai_document.AIServiceDocumentClientCompositeOperations(oci.ai_document.AIServiceDocumentClient(config=config))

    # Text extraction feature
    text_extraction_feature = oci.ai_document.models.DocumentTextExtractionFeature()

    # Setup the output location where processor job results will be created
    output_location = oci.ai_document.models.OutputLocation()
    output_location.namespace_name = "id09o3eaz21u"  # e.g. "axk2tfhlrens"
    output_location.bucket_name = "Buckettest"  # e.g "output"
    output_location.prefix = "stem"  # e.g "demo"

    # Create a processor_job for text_extraction feature
    create_processor_job_details_text_extraction = oci.ai_document.models.CreateProcessorJobDetails(
                                                        display_name=str(uuid.uuid4()),
                                                        compartment_id=COMPARTMENT_ID,
                                                        input_location=oci.ai_document.models.InlineDocumentContent(data=text_extraction_sample_string),
                                                        output_location=output_location,
                                                        processor_config=oci.ai_document.models.GeneralProcessorConfig(features=[text_extraction_feature]))

    print("Calling create_processor with create_processor_job_details_text_extraction:", create_processor_job_details_text_extraction)
    create_processor_response = aiservicedocument_client.create_processor_job_and_wait_for_state(
        create_processor_job_details=create_processor_job_details_text_extraction,
        wait_for_states=[oci.ai_document.models.ProcessorJob.LIFECYCLE_STATE_SUCCEEDED],
        waiter_kwargs={"wait_callback": create_processor_job_callback})

    print("processor call succeeded with status: {} and request_id: {}.".format(create_processor_response.status, create_processor_response.request_id))
    processor_job: oci.ai_document.models.ProcessorJob = create_processor_response.data
    print("create_processor_job_details_text_detection response: ", create_processor_response.data)

    print("Getting defaultObject.json from the output_location")
    object_storage_client = oci.object_storage.ObjectStorageClient(config=config)
    get_object_response = object_storage_client.get_object(namespace_name=output_location.namespace_name,
                                                        bucket_name=output_location.bucket_name,
                                                        object_name="{}/{}/_/results/defaultObject.json".format(
                                                            output_location.prefix, processor_job.id))
    return (str(get_object_response.data.content.decode()))
