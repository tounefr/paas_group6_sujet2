import kfp
from kfp import dsl
from kubernetes.client.models import V1EnvVar, V1SecretKeySelector

@dsl.pipeline(
    name='Sequential pipeline',
    description='A pipeline with two sequential steps.'
)
def sequential_pipeline(model_data_url = "https://test-epi.s3.fr-par.scw.cloud/kc_house_data.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=SCWTTHE3QW9915A46GMW%2F20200206%2Ffr-par%2Fs3%2Faws4_request&X-Amz-Date=20200206T200330Z&X-Amz-Expires=521789&X-Amz-Signature=56952a33bf8a12b255ed573a2a4e05dd901eec9985a98ed332f89c61ad55a2cd&X-Amz-SignedHeaders=host"):
    model_data_dest = "/data/kc_house_data.csv"

    vop = dsl.VolumeOp(
        name="vol",
        resource_name="newpvc",
        size="1Gi",
        modes=dsl.VOLUME_MODE_RWM
    )

    op_download = dsl.ContainerOp(
        name='download',
        image='toune/epi-saas-project2-download',
        pvolumes={"/data": vop.volume}
    )
    op_download.container.add_env_variable(V1EnvVar(name='DOWNLOAD_FILE_URL', value=model_data_url))
    op_download.container.add_env_variable(V1EnvVar(name='DOWNLOAD_FILE_DEST', value=model_data_dest))

    op_predict = dsl.ContainerOp(
        name='predict',
        image='toune/epi-saas-project2-app',
        pvolumes={"/data": vop.volume}
    )
    op_predict.container.add_env_variable(V1EnvVar(name='TRAINED_MODEL_PATH', value="/data/model-artifacts"))
    op_predict.container.add_env_variable(V1EnvVar(name='DATA_PATH', value=model_data_dest))

    op_predict.after(op_download)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(sequential_pipeline, __file__ + '.yaml')
